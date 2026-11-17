"""
URL configuration for file_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from core import settings

from django.conf.urls.static import static
from django.db.models import Count, Q
from django.views.generic import TemplateView
from apps.products.models import Product


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ۱. پرفروش‌ترین محصولات (بر اساس تعداد فروش در سفارش‌های paid)
        context["best_selling_products"] = (
            Product.objects.filter(is_active=True)
            .annotate(
                sales_count=Count(
                    "orderitem",
                    filter=Q(orderitem__order__status="paid")
                )
            )
            .order_by("-sales_count", "-created_at")[:4]
        )

        # ۲. جدیدترین محصولات
        context["newest_products"] = (
            Product.objects.filter(is_active=True)
            .order_by("-created_at")[:4]
        )

        # ۳. بخش مقالات / وبلاگ نمایشی (نمونه ثابت برای زیبایی صفحه اصلی)
        context["blog_posts"] = [
            {
                "title": "راهنمای جامع بهینه‌سازی و سئوی فایل‌های دانلودی",
                "date": "۲۵ آبان ۱۴۰۵",
                "excerpt": "نکاتی کلیدی برای افزایش فروش و جذب مشتری بیشتر برای محصولات دیجیتال در وب‌سایت...",
                "url": "#"
            },
            {
                "title": "چگونه امنیت محصولات دانلودی را در جنگو تضمین کنیم؟",
                "date": "۱۸ آبان ۱۴۰۵",
                "excerpt": "بررسی روش‌های امن‌سازی لینک‌های دانلود و جلوگیری از دسترسی غیرمجاز به فایل‌ها...",
                "url": "#"
            },
            {
                "title": "معرفی ابزارهای برتر برای طراحان و تولیدکنندگان محتوا",
                "date": "۱۰ آبان ۱۴۰۵",
                "excerpt": "مجموعه‌ای از کاربردی‌ترین ابزارها که روند تولید فایل و محتوای دیجیتال را تسریع می‌کنند...",
                "url": "#"
            },
        ]

        return context


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)