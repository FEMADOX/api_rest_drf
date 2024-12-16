from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from api.models import Category, Product
from api.serializers import (CategoryProductSerializer, CategorySerializer,
                             ProductSerializer)

# Create your views here.


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = "product_id"
    lookup_field = "title"

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get("lookup_value")

        try:
            obj = queryset.get(id=lookup_value)
        except (Product.DoesNotExist, ValueError):
            obj = get_object_or_404(queryset, title=lookup_value)
        return obj


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = "category_id"


class CategoryProductView(generics.RetrieveAPIView):
    serializer_class = CategoryProductSerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = "category_id"
