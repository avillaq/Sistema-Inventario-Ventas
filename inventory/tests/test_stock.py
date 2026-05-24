import pytest
from django.core.exceptions import ValidationError

from inventory.models import Product


@pytest.mark.django_db
def test_adjust_stock_rejects_negative():
    product = Product.objects.create(
        barcode="0001",
        name="Sample",
        cost="1.00",
        price="2.00",
        stock=0,
        min_stock=0,
    )

    with pytest.raises(ValidationError):
        product.adjust_stock(-1)


@pytest.mark.django_db
def test_is_low_stock_true_at_minimum():
    product = Product.objects.create(
        barcode="0002",
        name="Sample 2",
        cost="1.00",
        price="2.00",
        stock=5,
        min_stock=5,
    )

    assert product.is_low_stock is True
