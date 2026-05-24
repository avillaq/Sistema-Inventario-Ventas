from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    barcode = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(cost__gte=0),
                name="product_cost_non_negative",
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name="product_price_non_negative",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.barcode})"

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock

    def adjust_stock(self, delta):
        if delta == 0:
            return
        new_stock = self.stock + delta
        if new_stock < 0:
            raise ValidationError("Insufficient stock.")
        self.stock = new_stock
        self.save(update_fields=["stock", "updated_at"])


class StockAdjustment(models.Model):
    class AdjustmentType(models.TextChoices):
        LOSS = "LOSS", "Loss"
        RECEIPT = "RECEIPT", "Receipt"
        CORRECTION = "CORRECTION", "Correction"

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_adjustments",
    )
    adjustment_type = models.CharField(
        max_length=12,
        choices=AdjustmentType.choices,
        default=AdjustmentType.CORRECTION,
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reason = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stock_adjustments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} {self.adjustment_type} {self.quantity}"

    @property
    def signed_quantity(self):
        if self.adjustment_type == self.AdjustmentType.RECEIPT:
            return self.quantity
        return -self.quantity
