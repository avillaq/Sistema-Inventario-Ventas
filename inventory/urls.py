from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.inventory_overview, name="overview"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("search/", views.product_search, name="product_search"),
]
