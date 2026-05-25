import pytest
from django.urls import reverse


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("invalid_value", ["abc", "@@@"])
def test_inventory_stock_rejects_non_numeric_input_ui(live_server, page, invalid_value):
    page.goto(live_server.url + reverse("inventory:overview"))

    page.get_by_role("button", name="Nuevo producto").click()
    page.wait_for_selector("#inventory-modal-body input[name='barcode']")

    page.fill("input[name='barcode']", "UI-0001")
    page.fill("input[name='name']", "Producto UI")
    page.fill("input[name='cost']", "10.00")
    page.fill("input[name='price']", "15.00")
    stock_input = page.locator("input[name='stock']")
    stock_input.fill("0")
    stock_input.click()
    stock_input.type(invalid_value)
    page.fill("input[name='min_stock']", "1")

    value = stock_input.input_value()
    assert value == "0"


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("field_name", ["stock", "min_stock"])
@pytest.mark.parametrize(
    "value, expected_valid",
    [(-1, False), (0, True), (1, True), (9999, True), (10000, True), (10001, False)],
)
def test_inventory_stock_range_limits_ui(live_server, page, field_name, value, expected_valid):
    page.goto(live_server.url + reverse("inventory:overview"))

    page.get_by_role("button", name="Nuevo producto").click()
    page.wait_for_selector("#inventory-modal-body input[name='barcode']")

    input_field = page.locator(f"input[name='{field_name}']")
    input_field.fill(str(value))

    is_valid = input_field.evaluate("el => el.checkValidity()")
    assert is_valid is expected_valid
