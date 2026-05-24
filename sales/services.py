from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from inventory.models import Product

from .models import Sale, SaleItem, default_tax_rate

CENTS = Decimal("0.01")


def _normalize_items(items):
    if not isinstance(items, list) or not items:
        raise ValidationError("El carrito está vacío.")

    aggregated = {}

    for item in items:
        if not isinstance(item, dict):
            raise ValidationError("Datos del artículo inválidos.")
        try:
            product_id = int(item.get("product_id"))
            quantity = int(item.get("quantity"))
        except (TypeError, ValueError):
            raise ValidationError("Datos del artículo inválidos.")

        if product_id <= 0 or quantity <= 0:
            raise ValidationError("Cantidad inválida.")

        aggregated[product_id] = aggregated.get(product_id, 0) + quantity

    return aggregated


def _round_money(value):
    return value.quantize(CENTS)


def create_sale(*, cashier, items, tax_rate=None):
    if cashier is not None and not getattr(cashier, "is_authenticated", False):
        cashier = None

    normalized = _normalize_items(items)

    if tax_rate is None:
        tax_rate = default_tax_rate()

    if not isinstance(tax_rate, Decimal):
        try:
            tax_rate = Decimal(str(tax_rate))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError("Tasa de impuesto inválida.")

    if not tax_rate.is_finite() or tax_rate < 0:
        raise ValidationError("Tasa de impuesto inválida.")

    product_ids = list(normalized.keys())

    with transaction.atomic():
        products = Product.objects.select_for_update().filter(
            id__in=product_ids,
            is_active=True,
        )
        product_map = {product.id: product for product in products}

        if len(product_map) != len(product_ids):
            raise ValidationError("Algunos productos no están disponibles.")

        subtotal = Decimal("0.00")
        line_items = []

        for product_id, quantity in normalized.items():
            product = product_map[product_id]
            if product.stock < quantity:
                raise ValidationError(f"Stock insuficiente para {product.name}.")

            line_total = _round_money(product.price * quantity)
            subtotal += line_total
            line_items.append((product, quantity, line_total))

        tax_amount = _round_money(subtotal * tax_rate)
        total = _round_money(subtotal + tax_amount)

        sale = Sale.objects.create(
            cashier=cashier,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total=total,
        )

        for product, quantity, line_total in line_items:
            SaleItem.objects.create(
                sale=sale,
                product=product,
                product_name=product.name,
                unit_cost=product.cost,
                unit_price=product.price,
                quantity=quantity,
                line_total=line_total,
            )
            product.stock -= quantity
            product.save(update_fields=["stock", "updated_at"])

    return sale
