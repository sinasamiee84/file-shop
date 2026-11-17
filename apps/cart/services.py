from django.db import transaction
from .models import Cart, Order, OrderItem
from django.db.models import Max



@transaction.atomic
def create_order_from_cart(*, user, phone_number):
    cart = Cart.objects.prefetch_related("items__product").get(user=user)

    if not cart.items.exists():
        raise ValueError("سبد خرید شما خالی است.")
    max_num = Order.objects.filter(user=user).aggregate(
        max_num=Max("user_order_number")
    )["max_num"]

    next_order_number = (max_num or 0) + 1
    order = Order.objects.create(
        user=user,
        user_order_number=next_order_number,
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

