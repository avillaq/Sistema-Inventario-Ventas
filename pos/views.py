from django.conf import settings
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET

from inventory.models import Product
from sales.models import Sale, SaleItem


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


@require_GET
def dashboard(request):
    today = timezone.localdate()
    sales_today = Sale.objects.filter(
        status=Sale.Status.COMPLETED,
        created_at__date=today,
    )

    totals_today = sales_today.aggregate(
        total_amount=Sum("total"),
        total_count=Count("id"),
    )

    margin_expr = ExpressionWrapper(
        (F("unit_price") - F("unit_cost")) * F("quantity"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    margin_today = SaleItem.objects.filter(
        sale__status=Sale.Status.COMPLETED,
        sale__created_at__date=today,
    ).aggregate(margin=Sum(margin_expr))

    month_start = today.replace(day=1)
    top_products = (
        SaleItem.objects.filter(
            sale__status=Sale.Status.COMPLETED,
            sale__created_at__date__gte=month_start,
        )
        .values("product_id", "product_name")
        .annotate(quantity=Sum("quantity"), total=Sum("line_total"))
        .order_by("-quantity", "-total")[:5]
    )

    inventory_value = Product.objects.filter(is_active=True).aggregate(
        value=Sum(
            ExpressionWrapper(
                F("stock") * F("cost"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )

    low_stock_count = Product.objects.filter(
        is_active=True,
        stock__lte=F("min_stock"),
    ).count()

    context = {
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
        "totals_today": totals_today,
        "margin_today": margin_today,
        "inventory_value": inventory_value,
        "low_stock_count": low_stock_count,
        "top_products": top_products,
    }

    template = (
        "pos/partials/dashboard_content.html"
        if _is_htmx(request)
        else "pos/dashboard.html"
    )
    return render(request, template, context)
