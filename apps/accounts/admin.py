from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone_number", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        ("اطلاعات تماس", {"fields": ("phone_number",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("اطلاعات تماس", {"fields": ("phone_number",)}),
    )
