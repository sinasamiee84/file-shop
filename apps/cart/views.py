from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView

from apps.products.models import Product
from .models import Cart, CartItem
from .forms import CheckoutForm
from .services import create_order_from_cart


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        context["cart_items"]	 = cart.items.select_related("product")
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        # اگر کاربر پس از لاگین با متد GET به اینجا برگشت، هدایتش کن به صفحه جزئیات محصول یا سبد خرید
        product = get_object_or_404(Product, id=product_id)
        return redirect("products:detail", slug=product.slug)
    def post(self, request, product_id):
        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True,
        )

        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            messages.error(request, "تعداد محصول باید حداقل یک باشد.")
            return redirect("products:detail", slug=product.slug)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        messages.success(request, "محصول با موفقیت به سبد خرید اضافه شد.")

        # ماندن در صفحه محصول
        return redirect("products:detail", slug=product.slug)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        cart_item.delete()
        messages.success(request, "محصول از سبد خرید حذف شد.")

        return redirect("cart:detail")


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "cart/checkout.html"
    form_class = CheckoutForm

    def get_initial(self):
        initial = super().get_initial()
        if hasattr(self.request.user, "phone_number") and self.request.user.phone_number:
            initial["phone_number"] = self.request.user.phone_number
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # سبد خرید کاربر را پیدا می‌کنیم (بر اساس related_name یا پرس‌وجوی معمولی)
        # فرض بر این است که Cart رابطه one-to-one یا foreign key با user دارد
        cart = Cart.objects.filter(user=self.request.user).first()
        context["cart"] = cart
        # آیتم‌های سبد خرید همراه با محصول (برای جلوگیری از N+1 Query)
        context["cart_items"] = cart.items.select_related("product") if cart else []
        return context

    def form_valid(self, form):
        try:
            order = create_order_from_cart(
                user=self.request.user,
                phone_number=form.cleaned_data["phone_number"],
            )
        except ValueError as error:
            form.add_error(None, str(error))
            return self.form_invalid(form)

        return redirect("payment:start", order_id=order.id)




class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])
            messages.success(request, "تعداد محصول افزایش یافت.")
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save(update_fields=["quantity"])
                messages.success(request, "تعداد محصول کاهش یافت.")
            else:
                cart_item.delete()
                messages.success(request, "محصول از سبد خرید حذف شد.")
        elif action == "remove":
            cart_item.delete()
            messages.success(request, "محصول از سبد خرید حذف شد.")

        return redirect("cart:detail")
