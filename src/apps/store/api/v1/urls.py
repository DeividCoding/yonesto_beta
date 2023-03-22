# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path(
        "product/info/<code>/",
        views.ProductInfoView.as_view(),
        name="product-info-retrieve",
    ),
    path(
        "product/info/", views.ProductInfoListView.as_view(), name="product-info-list"
    ),
    path("buy/create/", views.BuyClientAPIView.as_view(), name="buy-create"),
    path("buy/info/", views.BuyTotalsAPI.as_view(), name="buy-info"),
    path("buy/revenue/", views.RevenueTotalAPI.as_view(), name="buy-revenue"),
]
