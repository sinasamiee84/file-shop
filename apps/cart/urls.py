from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    RemoveFromCartView,
    CheckoutView,
    UpdateCartItemView
)

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add"),
    path("remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove"),
    path("update/<int:item_id>/", UpdateCartItemView.as_view(), name="update"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    # صفحه‌ای که بعد از ثبت سفارش کاربر به آن می‌رود (در ادامه مدل یا ویوی جزئیات سفارش را هم اضافه می‌کنیم)
    # path("order/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
]
