from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import ProductForm
from .models import Brand, Category, Product


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _extract_filters(request):
    query = (
        request.POST.get("current_q")
        or request.GET.get("current_q")
        or request.GET.get("q")
        or ""
    ).strip()
    low_raw = (
        request.POST.get("current_low")
        or request.GET.get("current_low")
        or request.GET.get("low")
        or ""
    )
    low = str(low_raw) == "1"
    category = (
        request.POST.get("current_category")
        or request.GET.get("current_category")
        or request.GET.get("category")
        or ""
    ).strip()
    brand = (
        request.POST.get("current_brand")
        or request.GET.get("current_brand")
        or request.GET.get("brand")
        or ""
    ).strip()
    return query, low, category, brand


def _filtered_products(query, low_stock_only=False, category="", brand=""):
    products = Product.objects.select_related("category", "brand").filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(barcode__icontains=query)
        )

    if low_stock_only:
        products = products.filter(stock__lte=F("min_stock"))

    if category.isdigit():
        products = products.filter(category_id=int(category))

    if brand.isdigit():
        products = products.filter(brand_id=int(brand))

    return products


def _filter_choices():
    return {
        "categories": Category.objects.filter(is_active=True).order_by("name"),
        "brands": Brand.objects.filter(is_active=True).order_by("name"),
    }


@require_GET
def inventory_overview(request):
    query, low_stock_only, category, brand = _extract_filters(request)
    products = _filtered_products(query, low_stock_only, category, brand)
    product_count = products.count()
    products = products.order_by("name")[:200]

    context = {
        "products": products,
        "product_count": product_count,
        "filters": {
            "q": query,
            "low": "1" if low_stock_only else "",
            "category": category,
            "brand": brand,
        },
        "form": ProductForm(),
        "current_q": query,
        "current_low": "1" if low_stock_only else "",
        "current_category": category,
        "current_brand": brand,
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
        **_filter_choices(),
    }

    template = (
        "inventory/partials/overview_content.html"
        if _is_htmx(request)
        else "inventory/overview.html"
    )
    return render(request, template, context)


def _form_context(
    *,
    form,
    query,
    low_stock_only,
    category,
    brand,
    title,
    submit_label,
    product=None,
    message=None,
):
    return {
        "form": form,
        "form_title": title,
        "submit_label": submit_label,
        "product": product,
        "success_message": message,
        "current_q": query,
        "current_low": "1" if low_stock_only else "",
        "current_category": category,
        "current_brand": brand,
    }


def _table_context(query, low_stock_only, category, brand):
    products = _filtered_products(query, low_stock_only, category, brand)
    return {
        "products": products.order_by("name")[:200],
        "product_count": products.count(),
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
        "current_q": query,
        "current_low": "1" if low_stock_only else "",
        "current_category": category,
        "current_brand": brand,
    }


@require_http_methods(["GET", "POST"])
def product_create(request):
    query, low_stock_only, category, brand = _extract_filters(request)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                **_form_context(
                    form=ProductForm(),
                    query=query,
                    low_stock_only=low_stock_only,
                    category=category,
                    brand=brand,
                    title="Nuevo producto",
                    submit_label="Guardar",
                    message="Producto creado.",
                ),
                **_table_context(query, low_stock_only, category, brand),
            }
            return render(request, "inventory/partials/product_form_response.html", context)
    else:
        form = ProductForm()

    context = _form_context(
        form=form,
        query=query,
        low_stock_only=low_stock_only,
        category=category,
        brand=brand,
        title="Nuevo producto",
        submit_label="Guardar",
    )
    return render(request, "inventory/partials/product_form.html", context)


@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    query, low_stock_only, category, brand = _extract_filters(request)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            context = {
                **_form_context(
                    form=ProductForm(instance=product),
                    query=query,
                    low_stock_only=low_stock_only,
                    category=category,
                    brand=brand,
                    title="Editar producto",
                    submit_label="Actualizar",
                    product=product,
                    message="Producto actualizado.",
                ),
                **_table_context(query, low_stock_only, category, brand),
            }
            return render(request, "inventory/partials/product_form_response.html", context)
    else:
        form = ProductForm(instance=product)

    context = _form_context(
        form=form,
        query=query,
        low_stock_only=low_stock_only,
        category=category,
        brand=brand,
        title="Editar producto",
        submit_label="Actualizar",
        product=product,
    )
    return render(request, "inventory/partials/product_form.html", context)


@require_http_methods(["POST"])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    query, low_stock_only, category, brand = _extract_filters(request)
    product.delete()

    context = {
        **_form_context(
            form=ProductForm(),
            query=query,
            low_stock_only=low_stock_only,
            category=category,
            brand=brand,
            title="Nuevo producto",
            submit_label="Guardar",
            message="Producto eliminado.",
        ),
        **_table_context(query, low_stock_only, category, brand),
    }
    return render(request, "inventory/partials/product_form_response.html", context)


@require_GET
def product_search(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.select_related("category", "brand").filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(barcode__icontains=query)
            | Q(category__name__icontains=query)
            | Q(brand__name__icontains=query)
        )

    products = products.order_by("name")[:20]

    context = {
        "products": products,
        "query": query,
        "currency": getattr(settings, "POS_CURRENCY", "PEN"),
    }

    return render(request, "inventory/partials/product_results.html", context)
