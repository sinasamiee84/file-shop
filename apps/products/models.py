from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name="نامک (Slug)")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # به جای CASCADE از PROTECT استفاده کردم تا دسته‌بندی با محصولات پاک نشود
        related_name="products",
        verbose_name="دسته‌بندی"
    )
    title = models.CharField(max_length=150, verbose_name="نام محصول")
    slug = models.SlugField(max_length=170, unique=True, allow_unicode=True, verbose_name="نامک (Slug)")
    cover = models.ImageField(upload_to="products/covers/", blank=True, null=True, verbose_name="تصویر کاور")
    description = models.TextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت (تومان)")

    # فایل اصلی که قرار است فروخته شود
    file = models.FileField(upload_to="products/files/", verbose_name="فایل دانلودی")

    is_active = models.BooleanField(default=True, verbose_name="فعال / در دسترس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
