from django.urls import path

from api.views import (CategoryDetailView, CategoryProductView, CategoryView,
                       ProductDetailView, ProductView)

urlpatterns = [
    path("products/", ProductView.as_view(), name="all_products"),
    path("categories/", CategoryView.as_view(), name="all_categories"),
    # Dinamic Urls
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
        "categories/category/<int:category_id>/products",
        CategoryProductView.as_view(),
        name="products_by_category",
    ),
]
