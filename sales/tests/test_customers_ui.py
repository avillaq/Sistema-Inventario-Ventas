import pytest
from django.urls import reverse


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "document_id, expected_valid",
    [("1234567", False), ("12345678", True)],
)
def test_customers_document_id_length_ui(live_server, page, document_id, expected_valid):
    page.goto(live_server.url + reverse("sales:customers"))

    page.get_by_role("button", name="Nuevo cliente").click()
    page.wait_for_selector("#customer-modal-body input[name='full_name']")

    input_field = page.locator("input[name='document_id']")
    input_field.fill(document_id)

    is_valid = input_field.evaluate("el => el.checkValidity()")
    assert is_valid is expected_valid


@pytest.mark.django_db(transaction=True)
def test_customers_document_id_maxlength_ui(live_server, page):
    page.goto(live_server.url + reverse("sales:customers"))

    page.get_by_role("button", name="Nuevo cliente").click()
    page.wait_for_selector("#customer-modal-body input[name='full_name']")

    input_field = page.locator("input[name='document_id']")
    input_field.type("123456789")

    value = input_field.input_value()
    assert value == "12345678"


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "phone, expected_valid",
    [("12345678", False), ("123456789", True)],
)
def test_customers_phone_length_ui(live_server, page, phone, expected_valid):
    page.goto(live_server.url + reverse("sales:customers"))

    page.get_by_role("button", name="Nuevo cliente").click()
    page.wait_for_selector("#customer-modal-body input[name='full_name']")

    input_field = page.locator("input[name='phone']")
    input_field.fill(phone)

    is_valid = input_field.evaluate("el => el.checkValidity()")
    assert is_valid is expected_valid


@pytest.mark.django_db(transaction=True)
def test_customers_phone_maxlength_ui(live_server, page):
    page.goto(live_server.url + reverse("sales:customers"))

    page.get_by_role("button", name="Nuevo cliente").click()
    page.wait_for_selector("#customer-modal-body input[name='full_name']")

    input_field = page.locator("input[name='phone']")
    input_field.type("1234567890")

    value = input_field.input_value()
    assert value == "123456789"
