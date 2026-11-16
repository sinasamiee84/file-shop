from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "test@example.com"
        self.password = "SecretPassword123!"

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.register_url = reverse("accounts:register")

    def test_login_page_loads(self):
        """تست باز شدن صفحه لاگین"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        """تست ورود موفقیت‌آمیز"""
        response = self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """تست خروج از حساب کاربری (با متد POST)"""
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_register_page_loads(self):
        """تست باز شدن صفحه ثبت‌نام"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_register_functionality(self):
        """تست ثبت‌نام کاربر جدید و لاگین خودکار"""
        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "NewUserPass123!",
                "password2": "NewUserPass123!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser").exists())
