from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        "title",
        "category",
        "price_display",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "category", "created_at"]
    search_fields = ["title", "description", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_active"]  # تغییر سریع وضعیت فعال/غیرفعال از لیست
    list_per_page = 20

    # فرم‌بندی فیلدها در صفحه ویرایش محصول برای ظاهر تمیزتر
    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": ("title", "slug", "category", "price", "description"),
            },
        ),
        (
            "فایل و رسانه",
            {
                "fields": ("cover", "file"),
            },
        ),
        (
            "تنظیمات انتشار",
            {
                "fields": ("is_active",),
            },
        ),
    )

    @admin.display(description="قیمت (تومان)")
    def price_display(self, obj):
        # نمایش قیمت به صورت سه‌رقم سه‌رقم با ویرگول (مثلا 50,000)
        return f"{obj.price:,}"
