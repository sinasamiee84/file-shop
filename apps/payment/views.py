from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from apps.cart.models import Order ,Cart
from .models import Payment
from .services import send_zarinpal_request, verify_zarinpal_payment


class StartPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")

        # مبلغ سفارش (فرض بر این است که مبلغ بر حسب تومان است)
        amount = order.total_price
        description = f"پرداخت سفارش شماره {order.id}"

        # ساخت callback URL کامل با استفاده از domain جاری
        callback_url = request.build_absolute_uri(reverse("payment:verify"))

        success, result, payment_url = send_zarinpal_request(amount, description, callback_url)

        if success:
            # ذخیره یا به‌روزرسانی رکورد پرداخت
            Payment.objects.create(
                user=request.user,
                order=order,
                amount=amount,
                authority=result
            )
            return redirect(payment_url)
        else:
            # در صورت خطا در اتصال به درگاه
            return render(request, "payment/payment_error.html", {"error": result})


class VerifyPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        authority = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment = get_object_or_404(Payment, authority=authority, user=request.user)
        order = payment.order

        if status != "OK":
            payment.is_paid = False
            payment.save()
            order.status = "failed"
            order.save()
            return render(request, "payment/payment_failed.html", {"order": order})

        # تایید نهایی از سمت سرور
        success, ref_id_or_error = verify_zarinpal_payment(payment.amount, authority)

        if success:
            payment.is_paid = True
            payment.ref_id = str(ref_id_or_error)
            payment.save()

            # تغییر وضعیت سفارش به پرداخت شده
            order.status = "paid"
            order.save()

            # *** اینجا سبد خرید کاربر خالی می‌شود چون پرداخت قطعی و موفق بوده ***
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart.items.all().delete()

            return render(request, "payment/payment_success.html", {"order": order, "ref_id": payment.ref_id})
        else:
            payment.is_paid = False
            payment.save()
            order.status = "failed"
            order.save()
            return render(request, "payment/payment_failed.html", {"order": order, "error": ref_id_or_error})

