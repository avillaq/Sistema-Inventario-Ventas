import pytest
from django.urls import reverse
from playwright.sync_api import expect

from inventory.models import Product
from sales.models import Customer


@pytest.mark.django_db(transaction=True)
def test_pos_cart_caps_quantity_at_stock_ui(live_server, page):
    product = Product.objects.create(
        barcode="AAA-001",
        name="AAA Widget",
        cost="10.00",
        price="15.00",
        stock=2,
        min_stock=1,
        is_active=True,
    )
    Customer.objects.create(
        full_name="Cliente UI",
        document_id="12345678",
        email="",
        phone="987654321",
        is_active=True,
    )

    page.goto(live_server.url + reverse("sales:pos"))

    row = page.locator("tr:has-text('AAA Widget')")
    expect(row).to_be_visible()
    row.get_by_role("button", name="Agregar").click()

    qty_input = page.locator("tbody tr:has-text('AAA Widget') input[type='number']")
    expect(qty_input).to_have_value("1")

    qty_input.fill("5")
    qty_input.press("Tab")

    expect(qty_input).to_have_value(str(product.stock))

    plus_button = page.locator("tbody tr:has-text('AAA Widget') button:has-text('+')")
    expect(plus_button).to_be_disabled()

    message = page.locator("#checkout-message")
    expect(message).to_contain_text("Stock disponible alcanzado")
