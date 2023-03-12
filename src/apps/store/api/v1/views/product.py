from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.store.models.product import Buy, BuyProduct, PriceProduct, Product
from apps.store.models.users import UserClient

from ..serializers.product import BuyClientSerializer, ProductInfoSerializer


class ProductInfoView(generics.RetrieveAPIView):
    serializer_class = ProductInfoSerializer
    queryset = Product.objects.all()

    def get_object(self):
        code = self.kwargs.get("code")
        return get_object_or_404(Product, code=code)

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        latest_price = PriceProduct.objects.filter(product=instance).latest(
            "date_purchase"
        )
        data = serializer.data
        data["sale_price"] = latest_price.sale_price
        return Response(data)


class BuyClientAPIView(generics.CreateAPIView):
    serializer_class = BuyClientSerializer
    queryset = Buy.objects.all()
