from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.store.models.product import Buy, PriceProduct, Product
from apps.store.models.users import UserClient

from ..serializers.users import InfoUnPaidBuysClientSerializer, UserClientInfoSerializer


class UserClientInfoView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserClientInfoSerializer
    queryset = UserClient.available_objects.all()

    def get_object(self):
        code = self.kwargs.get("code")
        return get_object_or_404(UserClient, code=code)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data)


class UnPaidBuysUserClientInfoView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InfoUnPaidBuysClientSerializer
    queryset = UserClient.available_objects.all()

    def get_object(self):
        code = self.kwargs.get("code")
        return get_object_or_404(UserClient, code=code)

    def get(self, request, *args, **kwargs):
        user_client = self.get_object()
        buys = user_client.my_buys.prefetch_related(
            "my_buy_products__product", "my_buy_products__price_product"
        ).filter(remaining_amount__gt=0)

        total_remaining_amount = 0
        number_buys = 0
        for buy in buys:
            total_remaining_amount += buy.remaining_amount
            number_buys += 1
            buy.buy_products = buy.my_buy_products.all()

        serializer = self.get_serializer(
            {
                "number_buys": number_buys,
                "total_remaining_amount": total_remaining_amount,
                "buys": buys,
            }
        )
        return Response(serializer.data)
