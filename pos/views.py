import json
from datetime import timedelta

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import TruncDate
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
    week_start = today - timedelta(days=6)
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
    sales_last_week = (
        Sale.objects.filter(
            status=Sale.Status.COMPLETED,
            created_at__date__gte=week_start,
            created_at__date__lte=today,
        )
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total_amount=Sum("total"), total_count=Count("id"))
        .order_by("day")
    )
    sales_by_day = {row["day"]: row for row in sales_last_week}
    sales_last_7 = []
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        row = sales_by_day.get(day, {})
        total_amount = row.get("total_amount") or 0
        total_count = row.get("total_count") or 0
        sales_last_7.append(
            {
                "label": day.strftime("%d/%m"),
                "total": float(total_amount),
                "count": int(total_count),
            }
        )

    top_products = list(
        SaleItem.objects.filter(
            sale__status=Sale.Status.COMPLETED,
            sale__created_at__date__gte=month_start,
        )
        .values("product_id", "product_name")
        .annotate(quantity=Sum("quantity"), total=Sum("line_total"))
        .order_by("-quantity", "-total")[:5]
    )
    top_products_chart = [
        {
            "name": item["product_name"],
            "quantity": int(item["quantity"] or 0),
            "total": float(item["total"] or 0),
        }
        for item in top_products
    ]

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
        "sales_last_7_json": json.dumps(sales_last_7, cls=DjangoJSONEncoder),
        "top_products_chart_json": json.dumps(top_products_chart, cls=DjangoJSONEncoder),
    }

    template = (
        "pos/partials/dashboard_content.html"
        if _is_htmx(request)
        else "pos/dashboard.html"
    )
    return render(request, template, context)
