from django.db import models
from django.conf import settings
from apps.cart.models import Order  

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments", verbose_name="سفارش")
    amount = models.PositiveIntegerField(verbose_name="مبلغ (تومان)")
    authority = models.CharField(max_length=100, blank=True, null=True, verbose_name="اتوریتی زرین‌پال")
    ref_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="کد پیگیری بانک")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"پرداخت سفارش #{self.order.id} - {self.amount} تومان"

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
