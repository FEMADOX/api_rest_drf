from django.contrib import admin

from api.models import Category, Client, Order, Product, ProductOrder

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "price", "image"]
    readonly_fields = ["created", "updated"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]
    readonly_fields = ["created"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "email",
        "phone",
        "direction",
        "created",
    ]
    readonly_fields = ["created"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "client",
        "total_price",
        "created",
    ]
    readonly_fields = ["total_price", "created"]


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "order_price"]
    readonly_fields = ["order_price"]
