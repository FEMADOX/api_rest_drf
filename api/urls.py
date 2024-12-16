from django.urls import path

from api.views import (CategoryDetailView, CategoryProductView, CategoryView,
                       ProductDetailView, ProductView)

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("categories/", CategoryView.as_view()),
    # Dinamic Urls
    path(
        "products/product/<lookup_value>",
        ProductDetailView.as_view()
    ),
    path(
        "categories/category/<int:category_id>",
        CategoryDetailView.as_view()
    ),
    path(
        "categories/category/<int:category_id>/products",
        CategoryProductView.as_view()
    ),
]
