from django.contrib import admin

from .models import Customer, Sale, SaleItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "document_id", "email", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "document_id", "email")


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "cashier", "customer", "status", "total")
    list_filter = ("status", "created_at")
    date_hierarchy = "created_at"
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("sale", "product_name", "quantity", "unit_price", "line_total")
    search_fields = ("product_name",)
