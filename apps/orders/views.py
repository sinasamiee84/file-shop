from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from apps.cart.models import Order, OrderItem


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items__product")
        )


class SecureDownloadView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        order_item = get_object_or_404(
            OrderItem.objects.select_related("product", "order"),
            id=item_id,
            order__user=request.user,
            order__status="paid",
        )

        product = order_item.product

        if product is None or not product.file:
            raise Http404("فایل این محصول موجود نیست.")

        return FileResponse(
            product.file.open("rb"),
            as_attachment=True,
            filename=product.file.name.split("/")[-1],
        )
