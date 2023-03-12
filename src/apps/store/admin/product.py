from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.store.models import Buy, BuyProduct, PriceProduct, Product, SupplierProduct


class ProductAdmin(BaseAdmin):
    search_fields = ("code", "name")
    ordering = ("name",)
    list_display = (
        "code",
        "name",
        "stock",
        "purchase_price",
        "sale_price",
        "date_last_price_register",
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def date_last_price_register(self, obj):
        date = obj.prices.latest("id")
        if date:
            date = date.created
        else:
            date = None
        return date

    def purchase_price(self, obj):
        price = obj.prices.latest("id")
        if price:
            price = price.purchase_price
        else:
            price = None
        return price

    def sale_price(self, obj):
        price = obj.prices.latest("id")
        if price:
            price = price.sale_price
        else:
            price = None
        return price


class PriceProductAdmin(BaseAdmin):
    search_fields = ("product__name",)
    ordering = ("product__name", "created")
    list_display = ("purchase_price", "sale_price", "product")

    class Meta:
        verbose_name = "Price product"
        verbose_name_plural = "Price products"


class BuyAdmin(BaseAdmin):
    search_fields = ("user_client__name",)
    ordering = ("user_client__name", "date_purchase")
    list_filter = ("user_client__name",)
    list_display = ("user_client", "date_purchase", "amount", "remaining_amount")

    class Meta:
        verbose_name = "Buy"
        verbose_name_plural = "Buys"


class BuyProductAdmin(BaseAdmin):
    search_fields = ("buy__user_client__name", "product")
    ordering = ("buy__date_purchase", "product", "remaining_amount")
    list_filter = ("buy__user_client__name", "product", "buy__date_purchase")
    list_display = (
        "client",
        "date_purchase",
        "product",
        "price_per_product",
        "quantity",
        "amount",
        "remaining_amount",
    )

    class Meta:
        verbose_name = "Buy product"
        verbose_name_plural = "Buy products"

    def date_purchase(self, obj):
        return obj.buy.date_purchase

    def client(self, obj):
        return obj.buy.user_client

    def price_per_product(self, obj):
        return obj.price_product.sale_price


class SupplierProductAdmin(BaseAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    list_display = ("name",)

    class Meta:
        verbose_name = "Supplier product"
        verbose_name_plural = "Supliers products"


admin.site.register(Product, ProductAdmin)
admin.site.register(PriceProduct, PriceProductAdmin)
admin.site.register(Buy, BuyAdmin)
admin.site.register(BuyProduct, BuyProductAdmin)
admin.site.register(SupplierProduct, SupplierProductAdmin)
