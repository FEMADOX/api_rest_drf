from rest_framework import generics

from api.models import Category, Client, Order, Product
from api.serializers import (CategoryProductSerializer, CategorySerializer,
                             ClientSerializer, OrderSerializer,
                             ProductSerializer)

# Create your views here.


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ClientView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    lookup_url_kwarg = "client_id"
    serializer_class = ClientSerializer


class CategoryProductView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    lookup_url_kwarg = "category_id"
    serializer_class = CategoryProductSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
