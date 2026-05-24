import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

from inventory.forms import ProductForm
from inventory.models import Brand, Category, Product


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


@pytest.mark.django_db
def test_product_form_rejects_stock_above_business_limit():
    form = ProductForm(
        data={
            "barcode": "0003",
            "name": "Sample 3",
            "cost": "1.00",
            "price": "2.00",
            "stock": Product.MAX_STOCK + 1,
            "min_stock": "0",
            "is_active": "on",
        }
    )

    assert not form.is_valid()
    assert "stock" in form.errors


@pytest.mark.django_db
def test_inventory_overview_filters_by_category_and_brand(client):
    category = Category.objects.create(name="Bebidas")
    other_category = Category.objects.create(name="Limpieza")
    brand = Brand.objects.create(name="Andes")
    other_brand = Brand.objects.create(name="Costa")
    matching = Product.objects.create(
        barcode="1001",
        name="Agua",
        cost="1.00",
        price="2.00",
        stock=10,
        min_stock=2,
        category=category,
        brand=brand,
    )
    Product.objects.create(
        barcode="1002",
        name="Jabon",
        cost="1.00",
        price="2.00",
        stock=10,
        min_stock=2,
        category=other_category,
        brand=other_brand,
    )

    response = client.get(
        reverse("inventory:overview"),
        {"category": category.id, "brand": brand.id},
    )

    assert response.status_code == 200
    assert list(response.context["products"]) == [matching]
