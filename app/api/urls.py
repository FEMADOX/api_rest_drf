from django.urls import path

from api.views import (CategoryListView, CategoryProductView, ClientDetailView,
                       ClientView, OrderCreateView, ProductListView)

urlpatterns = [
    path("category/", CategoryListView.as_view()),
    path("category/<int:category_id>/products", CategoryProductView.as_view()),
    path("product/", ProductListView.as_view()),
    path("client/", ClientView.as_view()),
    path("client/<int:client_id>", ClientDetailView.as_view()),
    path("order/", OrderCreateView.as_view()),
]
