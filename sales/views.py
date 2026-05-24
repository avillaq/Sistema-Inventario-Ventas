import json
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from inventory.models import Product

from .forms import CustomerForm
from .models import Customer, Sale, default_tax_rate
from .services import create_sale


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _extract_customer_query(request):
    return (
        request.POST.get("current_q")
        or request.GET.get("current_q")
        or request.GET.get("q")
        or ""
    ).strip()


def _customer_queryset(query):
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            Q(full_name__icontains=query)
            | Q(document_id__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )

    return customers


@require_GET
def pos_screen(request):
    products = Product.objects.filter(is_active=True).order_by("name")[:12]
    context = {
        "products": products,
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
        "currency_decimals": getattr(settings, "POS_CURRENCY_DECIMALS", 2),
        "tax_rate": default_tax_rate(),
    }
    template = "sales/partials/pos_content.html" if _is_htmx(request) else "sales/pos.html"
    return render(request, template, context)


@require_POST
def checkout(request):
    items_raw = request.POST.get("items", "")

    if not items_raw:
        return render(
            request,
            "sales/partials/checkout_message.html",
            {"status": "error", "message": "No items in cart."},
        )

    try:
        items = json.loads(items_raw)
    except json.JSONDecodeError:
        return render(
            request,
            "sales/partials/checkout_message.html",
            {"status": "error", "message": "Invalid cart data."},
        )

    tax_rate_raw = request.POST.get("tax_rate", str(default_tax_rate()))
    try:
        tax_rate = Decimal(str(tax_rate_raw))
        if not tax_rate.is_finite():
            raise InvalidOperation
    except InvalidOperation:
        tax_rate = default_tax_rate()

    cashier = request.user if getattr(request.user, "is_authenticated", False) else None

    try:
        sale = create_sale(cashier=cashier, items=items, tax_rate=tax_rate)
    except ValidationError as exc:
        message = exc.message if hasattr(exc, "message") else "Sale failed."
        return render(
            request,
            "sales/partials/checkout_message.html",
            {"status": "error", "message": message},
        )

    response = render(
        request,
        "sales/partials/checkout_message.html",
        {"status": "success", "sale": sale},
    )
    response["HX-Trigger"] = json.dumps({"sale-completed": {"sale_id": sale.id}})
    return response


@require_GET
def sales_history(request):
    ticket = request.GET.get("ticket", "").strip()
    date_from_raw = request.GET.get("from", "").strip()
    date_to_raw = request.GET.get("to", "").strip()

    qs = Sale.objects.select_related("cashier", "customer").order_by("-created_at")

    if ticket.isdigit():
        qs = qs.filter(id=int(ticket))

    date_from = parse_date(date_from_raw) if date_from_raw else None
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)

    date_to = parse_date(date_to_raw) if date_to_raw else None
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    qs = qs.annotate(items_count=Count("items"))
    totals = qs.aggregate(total_amount=Sum("total"), total_count=Count("id"))

    context = {
        "sales": qs[:200],
        "filters": {
            "ticket": ticket,
            "from": date_from_raw,
            "to": date_to_raw,
        },
        "totals": totals,
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
    }
    template = (
        "sales/partials/history_content.html"
        if _is_htmx(request)
        else "sales/history.html"
    )
    return render(request, template, context)


def _customer_form_context(*, form, query, title, submit_label, customer=None, message=None):
    return {
        "form": form,
        "form_title": title,
        "submit_label": submit_label,
        "customer": customer,
        "success_message": message,
        "current_q": query,
    }


def _customer_table_context(query):
    customers = _customer_queryset(query)
    return {
        "customers": customers.order_by("full_name")[:200],
        "customer_count": customers.count(),
        "current_q": query,
    }


@require_GET
def customers_overview(request):
    query = _extract_customer_query(request)
    customers = _customer_queryset(query)

    context = {
        "customers": customers.order_by("full_name")[:200],
        "customer_count": customers.count(),
        "filters": {"q": query},
        "form": CustomerForm(),
        "current_q": query,
    }

    template = (
        "sales/partials/customers_content.html"
        if _is_htmx(request)
        else "sales/customers.html"
    )
    return render(request, template, context)


@require_http_methods(["GET", "POST"])
def customer_create(request):
    query = _extract_customer_query(request)

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                **_customer_form_context(
                    form=CustomerForm(),
                    query=query,
                    title="Nuevo cliente",
                    submit_label="Guardar",
                    message="Cliente creado.",
                ),
                **_customer_table_context(query),
            }
            return render(request, "sales/partials/customer_form_response.html", context)
    else:
        form = CustomerForm()

    context = _customer_form_context(
        form=form,
        query=query,
        title="Nuevo cliente",
        submit_label="Guardar",
    )
    return render(request, "sales/partials/customer_form.html", context)


@require_http_methods(["GET", "POST"])
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    query = _extract_customer_query(request)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            context = {
                **_customer_form_context(
                    form=CustomerForm(instance=customer),
                    query=query,
                    title="Editar cliente",
                    submit_label="Actualizar",
                    customer=customer,
                    message="Cliente actualizado.",
                ),
                **_customer_table_context(query),
            }
            return render(request, "sales/partials/customer_form_response.html", context)
    else:
        form = CustomerForm(instance=customer)

    context = _customer_form_context(
        form=form,
        query=query,
        title="Editar cliente",
        submit_label="Actualizar",
        customer=customer,
    )
    return render(request, "sales/partials/customer_form.html", context)


@require_http_methods(["POST"])
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    query = _extract_customer_query(request)
    customer.delete()

    context = {
        **_customer_form_context(
            form=CustomerForm(),
            query=query,
            title="Nuevo cliente",
            submit_label="Guardar",
            message="Cliente eliminado.",
        ),
        **_customer_table_context(query),
    }
    return render(request, "sales/partials/customer_form_response.html", context)
