from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Cart, CartItem, Order, OrderItem

# --- بخش سبد خرید (Cart) ---

class CartItemInline(TabularInline):
    model = CartItem
    extra = 0 # ردیف خالی اضافه نشان نده
    readonly_fields = ["total_price"] # فقط خواندنی چون محاسباتی است

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["user", "created_at", "total_price"]
    search_fields = ["user__username", "user__phone_number"]
    inlines = [CartItemInline]


# --- بخش سفارشات (Order) ---

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    # در سفارش، قیمت در زمان خرید هم مهم است
    readonly_fields = ["product", "price", "quantity"]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "user", "phone_number", "total_price", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "phone_number", "id"]
    list_editable = ["status"] # تغییر سریع وضعیت سفارش از لیست
    inlines = [OrderItemInline]

    # برای اینکه ادمین نتواند قیمت کل را دستی عوض کند و فاکتور خراب شود
    readonly_fields = ["created_at"]
