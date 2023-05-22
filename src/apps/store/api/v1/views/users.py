import threading
from decimal import Decimal

import pytz
from babel.dates import format_datetime
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.store.models.product import Buy, BuyProduct, PriceProduct, Product
from apps.store.models.users import UserClient
from apps.store.utils.ticket import Ticket
from config.settings.base import EMAIL_HOST_USER

from ..serializers.users import (
    BuysClientSerializer,
    InfoBuysPaymentClientSerializer,
    InfoUnPaidBuysClientSerializer,
    UserClientInfoSerializer,
)


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
        buys = (
            user_client.my_buys.prefetch_related(
                "my_buy_products__product", "my_buy_products__price_product"
            )
            .filter(remaining_amount__gt=0)
            .order_by("date_purchase", "remaining_amount")
        )
        total_remaining_amount = 0
        number_buys = 0
        for buy in buys:
            total_remaining_amount += buy.remaining_amount
            number_buys += 1
            buy.buy_products = buy.my_buy_products.all().order_by("remaining_amount")

        serializer = self.get_serializer(
            {
                "number_buys": number_buys,
                "total_remaining_amount": total_remaining_amount,
                "buys": buys,
            }
        )
        return Response(serializer.data)


class HistoryPayBuysClientView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BuysClientSerializer
    queryset = UserClient.available_objects.all()

    def generate_report(self, user_client, multiple_buys):
        print("Creando reporte")
        if user_client.email:
            print(f"Email:{user_client.email}")
            ticket = Ticket(
                username=f"{user_client.name}",
                multiple_buys=multiple_buys,
                user_email=user_client.email,
                user_name=user_client.name,
            )
            ticket.generate_tickets_and_send_mail(
                filename=f"history_payments_{user_client.name}.pdf"
            )

    def get_object(self):
        code = self.kwargs.get("code")
        return get_object_or_404(UserClient, code=code)

    def get(self, request, *args, **kwargs):
        user_client = self.get_object()
        buys = user_client.my_buys.all().order_by("date_purchase")
        for buy in buys:
            buy_products = buy.my_buy_products.all().order_by("remaining_amount")
            buy.buy_products = buy_products
        serializer = BuysClientSerializer(list(buys), many=True)

        report_thread = threading.Thread(
            target=self.generate_report, args=(user_client, serializer.data)
        )
        report_thread.start()

        return Response({"message": "El reporte se está generando en segundo plano."})


class PayBuysUserClientView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "payment": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=["code", "payment"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "total_buys_paid": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "paid_buys": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                    ),
                    "partially_paid_buy": openapi.Schema(type=openapi.TYPE_OBJECT),
                },
            ),
            400: "Bad request",
        },
        operation_summary="Pay user buys",
        operation_description="Pay the user buys with the given payment amount",
    )
    @transaction.atomic
    def post(self, request):
        user_code = request.data.get("code")
        payment = Decimal(request.data.get("payment"))
        payment_aux_client = payment
        user_client = get_object_or_404(UserClient, code=user_code)

        buys = user_client.my_buys.filter(remaining_amount__gt=0).order_by(
            "date_purchase"
        )
        buys_to_update = []
        buys_product_to_update = []

        partially_paid_buy = None
        paid_buys = []
        total_buys_paid = 0
        for buy in buys:
            if payment <= 0:
                break

            buy_products = buy.my_buy_products.all().order_by("remaining_amount")
            buy.buy_products = buy_products
            payment_aux_for_products = payment
            # update buy_products
            for buy_product in buy_products:
                buy_product.remaining_amount = Decimal(buy_product.remaining_amount)
                if payment_aux_for_products <= 0:
                    break
                remaining_product_amount = buy_product.remaining_amount
                if payment_aux_for_products >= remaining_product_amount:
                    payment_aux_for_products -= remaining_product_amount
                    buy_product.remaining_amount = 0
                else:
                    buy_product.remaining_amount -= payment_aux_for_products
                    payment_aux_for_products = 0
                buys_product_to_update.append(buy_product)

            # update buy
            buy.remaining_amount = Decimal(buy.remaining_amount)
            remaining_buy_amount = buy.remaining_amount
            buy.prev_remaining_amount = remaining_buy_amount
            if payment >= remaining_buy_amount:
                total_buys_paid += 1
                payment -= remaining_buy_amount
                buy.remaining_amount = 0
                paid_buys.append(buy)
            else:
                buy.remaining_amount -= payment
                partially_paid_buy = buy
                payment = 0
            buys_to_update.append(buy)

        # update on db: BuyProduct(s) and Buy(s)
        BuyProduct.objects.bulk_update(buys_product_to_update, ["remaining_amount"])
        Buy.objects.bulk_update(buys_to_update, ["remaining_amount"])

        # Send email
        if user_client.email:
            total_remaining_amount = (
                Buy.available_objects.filter(user_client=user_client).aggregate(
                    Sum("remaining_amount")
                )["remaining_amount__sum"]
                or 0
            )
            user_name = user_client.name
            user_email = user_client.email
            subject = f"Confirmación de pago en UNICAPP - Gracias,{user_name}!"

            message = f"""Hola,{user_name},

Nos complace informarte que hemos recibido tu pago de: ${payment_aux_client} y se ha aplicado correctamente a tu saldo pendiente en UNICAPP.

"""

            if total_remaining_amount == 0:
                message += "¡Felicidades! Has liquidado tu saldo pendiente por completo. Agradecemos tu preferencia y esperamos seguir siendo tu opción preferida para futuras compras."
            else:
                message += f"Excelente, gracias por abonar parte del dinero pendiente. Recuerda que en tu saldo pendiente aún quedan ${total_remaining_amount} MNX por pagar. Agradecemos tu preferencia y te animamos a ponerte al día con tus pagos para disfrutar al máximo de tu experiencia en UNICAPP."

            message += """
Si tienes alguna pregunta o inquietud sobre tu pago, no dudes en ponerte en contacto con el equipo de UNICAPP. Estaremos encantados de ayudarte.

¡Que tengas un excelente día!
            """

            sender_email = EMAIL_HOST_USER
            destination_emails = [
                user_email,
            ]
            send_mail(subject, message, sender_email, destination_emails)

        serializer = InfoBuysPaymentClientSerializer(
            {
                "total_buys_paid": total_buys_paid,
                "paid_buys": paid_buys,
                "partially_paid_buy": partially_paid_buy,
            }
        )

        return Response(serializer.data)
