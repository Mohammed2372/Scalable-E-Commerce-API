from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}  # auto fill slug when typing name


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "price", "stock", "category", "updated_at"]
    list_filter = ["category", "created_at"]
    list_editable = ["price", "stock"]  # edit price directly from the list view
    prepopulated_fields = {"slug": ("name",)}
