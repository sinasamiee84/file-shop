import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.products.models import Category, Product


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductModelTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.category = Category.objects.create(
            name="جزوه‌ها",
            slug="جزوه‌ها",
        )

        self.cover_file = SimpleUploadedFile(
            name="cover.jpg",
            content=(
                b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01"
                b"\x00\x00\x01\x00\x01\x00\x00"
            ),
            content_type="image/jpeg",
        )

        self.download_file = SimpleUploadedFile(
            name="differential.pdf",
            content=b"fake pdf file content",
            content_type="application/pdf",
        )

        self.product = Product.objects.create(
            category=self.category,
            title="جزوه دیفرانسیل",
            slug="جزوه-دیفرانسیل",
            cover=self.cover_file,
            description="توضیحات جزوه دیفرانسیل",
            price=50000,
            file=self.download_file,
            is_active=True,
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.title, "جزوه دیفرانسیل")
        self.assertEqual(self.product.price, 50000)
        self.assertTrue(self.product.is_active)

    def test_product_str(self):
        self.assertEqual(str(self.product), "جزوه دیفرانسیل")

    def test_product_belongs_to_category(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.category.products.count(), 1)

    def test_product_files_are_saved(self):
        self.assertTrue(self.product.cover.name.startswith("products/covers/"))
        self.assertTrue(self.product.file.name.startswith("products/files/"))

    def test_product_default_values(self):
        product = Product.objects.create(
            category=self.category,
            title="محصول بدون قیمت",
            slug="محصول-بدون-قیمت",
            description="توضیحات محصول",
            file=SimpleUploadedFile(
                name="empty-file.txt",
                content=b"test",
                content_type="text/plain",
            ),
        )

        self.assertEqual(product.price, 0)
        self.assertTrue(product.is_active)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductListViewTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.category = Category.objects.create(
            name="جزوه‌ها",
            slug="جزوه‌ها",
        )

        self.product_file = SimpleUploadedFile(
            name="product.txt",
            content=b"test product file",
            content_type="text/plain",
        )

    def create_product(
        self,
        title,
        slug,
        is_active=True,
    ):
        return Product.objects.create(
            category=self.category,
            title=title,
            slug=slug,
            description=f"توضیحات {title}",
            price=50000,
            file=SimpleUploadedFile(
                name=f"{slug}.txt",
                content=b"test file",
                content_type="text/plain",
            ),
            is_active=is_active,
        )

    def test_product_list_url_returns_200(self):
        response = self.client.get(reverse("products:list"))

        self.assertEqual(response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        response = self.client.get(reverse("products:list"))

        self.assertTemplateUsed(
            response,
            "products/product_list.html",
        )

    def test_only_active_products_are_displayed(self):
        active_product = self.create_product(
            title="محصول فعال",
            slug="محصول-فعال",
            is_active=True,
        )

        inactive_product = self.create_product(
            title="محصول غیرفعال",
            slug="محصول-غیرفعال",
            is_active=False,
        )

        response = self.client.get(reverse("products:list"))

        products = response.context["products"]

        self.assertIn(active_product, products)
        self.assertNotIn(inactive_product, products)
        self.assertContains(response, "محصول فعال")
        self.assertNotContains(response, "محصول غیرفعال")

    def test_product_list_is_paginated(self):
        for number in range(13):
            self.create_product(
                title=f"محصول {number}",
                slug=f"محصول-{number}",
            )

        response = self.client.get(reverse("products:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["products"]), 12)

    def test_second_page_contains_remaining_products(self):
        for number in range(13):
            self.create_product(
                title=f"محصول {number}",
                slug=f"محصول-{number}",
            )

        response = self.client.get(
            reverse("products:list"),
            {"page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 1)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductDetailViewTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.category = Category.objects.create(
            name="جزوه‌ها",
            slug="جزوه‌ها",
        )

        self.product = Product.objects.create(
            category=self.category,
            title="جزوه دیفرانسیل",
            slug="جزوه-دیفرانسیل",
            description="توضیحات جزوه دیفرانسیل",
            price=50000,
            file=SimpleUploadedFile(
                name="differential.pdf",
                content=b"fake pdf content",
                content_type="application/pdf",
            ),
            is_active=True,
        )

    def test_product_detail_url_returns_200(self):
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": self.product.slug},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_product_detail_uses_correct_template(self):
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": self.product.slug},
            )
        )

        self.assertTemplateUsed(
            response,
            "products/product_detail.html",
        )

    def test_product_detail_contains_product_data(self):
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": self.product.slug},
            )
        )

        self.assertEqual(response.context["product"], self.product)
        self.assertContains(response, "جزوه دیفرانسیل")
        self.assertContains(response, "توضیحات جزوه دیفرانسیل")
        self.assertContains(response, "50000")

    def test_product_detail_supports_persian_slug(self):
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": "جزوه-دیفرانسیل"},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_nonexistent_product_returns_404(self):
        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": "محصول-وجود-ندارد"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_inactive_product_detail_is_currently_accessible(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active"])

        response = self.client.get(
            reverse(
                "products:detail",
                kwargs={"slug": self.product.slug},
            )
        )

        self.assertEqual(response.status_code, 200)
