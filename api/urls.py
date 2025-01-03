from django.urls import path

from api.views import (CategoryDetailView, CategoryProductView, CategoryView,
                       ClientDetailView, ClientOrderView, ClientView,
                       OrderCreateView, ProductDetailView, ProductView)

urlpatterns = [
    path("products/", ProductView.as_view(), name="all_products"),
    path("categories/", CategoryView.as_view(), name="all_categories"),
    path("clients/", ClientView.as_view(), name="all_clients"),

    # Detail Urls
    path(
        "products/product/<lookup_value>",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "categories/category/<int:category_id>",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "client/<int:client_id>/",
        ClientDetailView.as_view(),
        name="client_detail",
    ),

    # Relationship Urls

    # Category
    path(
        "categories/category/<int:category_id>/products",
        CategoryProductView.as_view(),
        name="products_by_category",
    ),

    # Client
    path(
        "client/<int:client_id>/order/",
        ClientOrderView.as_view(),
        name="client_order",
    ),
    path(
        "client/<int:client_id>/add_order/",
        OrderCreateView.as_view(),
        name="create_order",
    ),
]
