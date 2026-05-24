import pytest
from django.core.exceptions import ValidationError

from inventory.models import Product
from sales.models import Sale
from sales.services import create_sale


@pytest.mark.django_db
def test_create_sale_rejects_quantity_above_stock():
    product = Product.objects.create(
        barcode="2001",
        name="Cafe",
        cost="5.00",
        price="8.00",
        stock=10,
        min_stock=2,
    )

    with pytest.raises(ValidationError):
        create_sale(cashier=None, items=[{"product_id": product.id, "quantity": 11}])

    product.refresh_from_db()
    assert product.stock == 10
    assert Sale.objects.count() == 0


@pytest.mark.django_db
def test_create_sale_accepts_stock_boundary_and_decrements_stock():
    product = Product.objects.create(
        barcode="2002",
        name="Te",
        cost="3.00",
        price="5.00",
        stock=10,
        min_stock=2,
    )

    sale = create_sale(
        cashier=None,
        items=[{"product_id": product.id, "quantity": 10}],
        tax_rate="0.18",
    )

    product.refresh_from_db()
    assert product.stock == 0
    assert sale.items.count() == 1
    assert sale.subtotal == product.price * 10
