from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.products.models import Category, Product
from apps.cart.models import Cart, CartItem, Order
from apps.cart.services import create_order_from_cart


class CartAndOrderTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number="09123456789", password="password123", username="تست‌کاربر"
        )
        self.category = Category.objects.create(name="فایل آموزشی", slug="edu-files")
        self.product = Product.objects.create(
            category=self.category,
            title="آموزش جنگو",
            slug="django-tutorial",
            price=150000,
            is_active=True,
        )

    def test_add_to_cart_and_order_creation(self):
        # تست افزودن به سبد خرید
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        self.assertEqual(cart.items.count(), 1)

        # تست ایجاد سفارش و شماره سفارش ترتیبی کاربر
        order = create_order_from_cart(user=self.user, phone_number=self.user.phone_number)

        self.assertEqual(order.user_order_number, 1)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().price, 150000)

        # ایجاد سفارش دوم برای بررسی ترتیبی بودن شماره سفارش کاربر
        cart2, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart2, product=self.product, quantity=1)

        order2 = create_order_from_cart(user=self.user, phone_number=self.user.phone_number)
        self.assertEqual(order2.user_order_number, 2)
