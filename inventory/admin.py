from django.contrib import admin

from .models import Brand, Category, Product, StockAdjustment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "barcode",
        "name",
        "price",
        "stock",
        "min_stock",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "category", "brand")
    search_fields = ("barcode", "name")
    autocomplete_fields = ("category", "brand")


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "adjustment_type",
        "quantity",
        "created_by",
        "created_at",
    )
    list_filter = ("adjustment_type", "created_at")
    search_fields = ("product__name", "product__barcode")
