from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active", "image_key")
    list_filter = ("category", "is_active")
    search_fields = ("name", "short")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user", "status", "customer_name", "phone", "total")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone", "address", "user__username", "user__email")
    inlines = (OrderItemInline,)
