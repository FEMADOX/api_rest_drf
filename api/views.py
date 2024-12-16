from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination

from api.models import Category, Product
from api.serializers import CategorySerializer, ProductSerializer

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
            try:
                obj = queryset.get(title=lookup_value)
            except Product.DoesNotExist:
                raise status.HTTP_404_NOT_FOUND
        return obj


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = "category_id"
