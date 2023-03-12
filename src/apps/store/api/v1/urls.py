# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("product/info/<code>/", views.ProductInfoView.as_view(), name="product-info"),
    path("buy/create/", views.BuyClientAPIView.as_view(), name="buy-create"),
]
