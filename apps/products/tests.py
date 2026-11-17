from django.test import TestCase
from django.urls import reverse
from apps.products.models import Category, Product


class ProductListViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="دسته تست", slug="test-cat")
        for i in range(10):
            Product.objects.create(
                category=self.category,
                title=f"محصول {i}",
                slug=f"product-{i}",
                price=1000,
                is_active=True
            )
        self.inactive_product = Product.objects.create(
            category=self.category,
            title="محصول غیرفعال",
            slug="inactive-prod",
            price=1000,
            is_active=False
        )

    def test_product_list_view_status_code(self):
        # تغییر 'product_list' به 'list' بر اساس apps/products/urls.py
        response = self.client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_list.html")

    def test_only_active_products_in_categories(self):
        """تست اینکه فقط محصولات فعال در دسته‌بندی‌ها نمایش داده می‌شوند"""
        response = self.client.get(reverse("products:list"))
        categories = response.context["categories"]

        for category in categories:
            for product in category.active_products:
                self.assertTrue(product.is_active)
            self.assertNotIn(self.inactive_product, category.active_products)

    def test_search_functionality(self):
        """تست جستجو با پارامتر q"""
        response = self.client.get(reverse("products:list"), {'q': 'محصول 1'})
        categories = response.context["categories"]
        for cat in categories:
            for prod in cat.active_products:
                self.assertIn('محصول 1', prod.title)
