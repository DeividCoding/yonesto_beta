from common.abstract_models import BaseModelClass
from django.db import models

from .users import UserClient


class SupplierProduct(BaseModelClass):
    name = models.CharField(verbose_name="Name:", max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModelClass):
    code = models.CharField(verbose_name="Code:", max_length=100, unique=True)
    name = models.CharField(verbose_name="Name:", max_length=50, unique=True)
    stock = models.IntegerField(verbose_name="Stock: ")

    def __str__(self):
        return f"{self.name}"


class PriceProduct(BaseModelClass):
    purchase_price = models.FloatField(verbose_name="Purchase price amount: ")
    sale_price = models.FloatField(verbose_name="Sale price amount: ")
    product = models.ForeignKey(
        Product,
        verbose_name="Product: ",
        on_delete=models.CASCADE,
        related_name="prices",
    )
    supplier = models.ForeignKey(
        SupplierProduct,
        verbose_name="Supplier",
        on_delete=models.CASCADE,
        related_name="prices",
    )
    date_purchase = models.DateField(verbose_name="Date purchase: ")

    def __str__(self):
        return f"{self.product} - Purchase: {self.purchase_price} - Sale: {self.sale_price}"


class Buy(BaseModelClass):
    date_purchase = models.DateTimeField()
    remaining_amount = models.FloatField(verbose_name="Remaining amount: ")
    amount = models.FloatField(verbose_name="Amount: ")
    user_client = models.ForeignKey(
        UserClient,
        verbose_name="Client: ",
        on_delete=models.CASCADE,
        related_name="my_buys",
    )

    def __str__(self):
        return f"{self.date_purchase} - {self.user_client.name} - Total cost: {self.amount}"


class BuyProduct(BaseModelClass):
    buy = models.ForeignKey(
        Buy, on_delete=models.CASCADE, related_name="my_buy_products"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="my_buy_products"
    )
    price_product = models.ForeignKey(
        PriceProduct, on_delete=models.CASCADE, related_name="my_buy_products"
    )
    quantity = models.IntegerField(verbose_name="Quantity of products purchased: ")
    remaining_amount = models.FloatField(verbose_name="Remaining amount: ")
    amount = models.FloatField(verbose_name="Amount: ")

    def __str__(self):
        return f"{self.buy.date_purchase} - {self.product.name} - Amount: {self.amount} - Remaining amount: {self.remaining_amount}"
