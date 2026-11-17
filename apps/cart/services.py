from django.db import transaction
from .models import Cart, Order, OrderItem


@transaction.atomic
def create_order_from_cart(*, user, phone_number):
    cart = Cart.objects.prefetch_related("items__product").get(user=user)

    if not cart.items.exists():
        raise ValueError("سبد خرید شما خالی است.")

    order = Order.objects.create(
        user=user,
        total_price=cart.total_price,
        phone_number=phone_number,
        status="pending",
    )

    order_items = [
        OrderItem(
            order=order,
            product=cart_item.product,
            price=cart_item.product.price,
            quantity=cart_item.quantity,
        )
        for cart_item in cart.items.all()
    ]
    OrderItem.objects.bulk_create(order_items)

    return order

