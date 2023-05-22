# Django
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "users/info/<code>/",
        views.UserClientInfoView.as_view(),
        name="userclient-info",
    ),
    path(
        "users/unpaid-buys/<code>/",
        views.UnPaidBuysUserClientInfoView.as_view(),
        name="userclient-unpaidbuys-info",
    ),
    path(
        "users/report-buys/<code>/",
        views.HistoryPayBuysClientView.as_view(),
        name="userclient-report-buys",
    ),
    path(
        "users/pay-buys",
        views.PayBuysUserClientView.as_view(),
        name="userclient-paybuys",
    ),
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
