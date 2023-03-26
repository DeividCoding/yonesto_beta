import pytz
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.store.models.product import Buy, BuyProduct, PriceProduct, Product
from apps.store.models.users import UserClient


class UserClientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = ("id", "name", "code", "email", "image", "remaining_credit")


class BuyProductClientSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField(source="product.image")
    product_name = serializers.ReadOnlyField(source="product.name")
    price_product_sale_price = serializers.ReadOnlyField(
        source="price_product.sale_price"
    )

    class Meta:
        model = BuyProduct
        fields = (
            "product_name",
            "quantity",
            "price_product_sale_price",
            "amount",
            "remaining_amount",
            "product_image",
        )

    def get_product_image(self, obj):
        request = self.context.get("request")
        if obj.product.image:
            return request.build_absolute_uri(obj.product.image.url)
        return None


class BuysClientSerializer(serializers.ModelSerializer):
    buy_products = BuyProductClientSerializer(many=True)
    date_purchase = serializers.SerializerMethodField()

    class Meta:
        model = Buy
        fields = (
            "date_purchase",
            "amount",
            "remaining_amount",
            "amount",
            "buy_products",
        )

    def get_date_purchase(self, obj):
        time_zone_convetion = pytz.timezone(settings.TIME_ZONE)
        date_purchase = obj.date_purchase.astimezone(time_zone_convetion)
        date_purchase_str = date_purchase.strftime("%Y-%m-%d %I:%M:%S %p")
        return date_purchase_str


class InfoUnPaidBuysClientSerializer(serializers.Serializer):
    total_remaining_amount = serializers.FloatField()
    number_buys = serializers.FloatField()
    buys = BuysClientSerializer(many=True)
