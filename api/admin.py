from django.contrib import admin

from api.models import Category, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "price", "image"]
    readonly_fields = ["created", "updated"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]
    readonly_fields = ["created"]
