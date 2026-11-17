from django.urls import path
from .views import StartPaymentView, VerifyPaymentView

app_name = "payment"

urlpatterns = [
    path("start/<int:order_id>/", StartPaymentView.as_view(), name="start"),
    path("verify/", VerifyPaymentView.as_view(), name="verify"),
]
