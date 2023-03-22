import pytz
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from apps.store.models.product import Buy, BuyProduct, PriceProduct, Product
from apps.store.models.users import UserClient


class BuyTotalsSerializer(serializers.Serializer):
    # total sale money
    total_amount = serializers.FloatField()
    total_remaining_amount = serializers.FloatField()
    total_recovered = serializers.FloatField()


class RevenueTotalsSerializer(serializers.Serializer):
    # total sale money
    total_expected_revenue = serializers.FloatField()
    total_potential_revenue = serializers.FloatField()
    total_revenue = serializers.FloatField()


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = ["date_purchase", "remaining_amount", "amount", "user_client"]


class ProductInfoSerializer(serializers.ModelSerializer):
    sale_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "code", "name", "stock", "sale_price", "image"]


class BuyClientProductSerializer(serializers.ModelSerializer):
    # debe existir un precio definido al producto
    # quantity debe ser mayo a cero

    # quantity debe ser mayor a cero
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = BuyProduct
        fields = ("product", "quantity")

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        if quantity > product.stock:
            raise serializers.ValidationError(
                {
                    "product": f"You want {quantity} {product.name}, but there is only {product.stock} {product.name}, that is, there is not enough stock for the product {product.name}"
                }
            )

        return data


class BuyClientSerializer(serializers.Serializer):
    client_code = serializers.IntegerField()
    payment = serializers.FloatField()
    products = BuyClientProductSerializer(many=True)

    def validate(self, data):
        client_code = data["client_code"]
        user_client = UserClient.objects.filter(code=client_code)
        if not user_client.exists():
            raise serializers.ValidationError(
                {"client_code": f"There is no user with code {client_code}"}
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        payment_client = validated_data["payment"]
        client_code = validated_data["client_code"]
        user_client = UserClient.objects.get(code=client_code)

        buy_instance, _ = Buy.objects.get_or_create(
            user_client=user_client,
            date_purchase=timezone.now(),
            amount=0,
            remaining_amount=0,
        )
        buy_total_amount = 0
        remaining_amount_buy_total = 0

        # Crea instancias de BuyProduct y actualiza los stocks de los productos
        buy_products = []
        products_to_update_stock = []
        for product_data in validated_data["products"]:
            product = product_data["product"]
            quantity = product_data["quantity"]
            price_product = PriceProduct.objects.filter(product=product).latest(
                "date_purchase"
            )

            sale_price_product = price_product.sale_price
            amount_product = sale_price_product * quantity
            remaining_amount_product = amount_product

            if payment_client > 0:
                remaining_amount_product -= payment_client
                if remaining_amount_product <= 0:
                    payment_client = abs(remaining_amount_product)
                    remaining_amount_product = 0
                else:
                    payment_client = 0
                    remaining_amount_buy_total = abs(remaining_amount_product)
            else:
                remaining_amount_buy_total += amount_product
            buy_total_amount += amount_product

            buy_products.append(
                BuyProduct(
                    buy=buy_instance,
                    product=product,
                    price_product=price_product,
                    quantity=quantity,
                    remaining_amount=remaining_amount_product,
                    amount=amount_product,
                )
            )

            product.stock = product.stock - quantity
            products_to_update_stock.append(product)

        buy_instance.remaining_amount = remaining_amount_buy_total
        buy_instance.amount = buy_total_amount
        buy_instance.save()
        BuyProduct.objects.bulk_create(buy_products)
        Product.objects.bulk_update(products_to_update_stock, ["stock"])

        return buy_instance

    def to_representation(self, instance):
        time_zone_convetion = pytz.timezone(settings.TIME_ZONE)
        data = {
            "user_client": str(instance.user_client),
            "user_code": str(instance.user_client.code),
            "date_purchase": instance.date_purchase.astimezone(
                time_zone_convetion
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "remaining_amount": instance.remaining_amount,
            "amount": instance.amount,
        }
        return data
