from django.urls import path

from .views import (
    OrderDetailView,
    SecureDownloadView,
    UserOrderListView,
)

app_name = "orders"

urlpatterns = [
    path("", UserOrderListView.as_view(), name="list"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="detail"),
    path(
        "download/<int:item_id>/",
        SecureDownloadView.as_view(),
        name="secure_download",
    ),
]
