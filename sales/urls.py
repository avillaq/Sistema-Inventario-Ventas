from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path("", views.pos_screen, name="pos"),
    path("checkout/", views.checkout, name="checkout"),
    path("history/", views.sales_history, name="history"),
    path("history/<int:pk>/detail/", views.sale_detail, name="sale_detail"),
    path("customers/", views.customers_overview, name="customers"),
    path("customers/new/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customer_edit"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customer_delete"),
]
