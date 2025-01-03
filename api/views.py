from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.models import Category, Client, Order, Product
from api.permissions import IsAdminOrReadOnly, IsClientOrAdmin
from api.serializers import (CategoryProductSerializer, CategorySerializer,
                             ClientOrderSerializer, ClientSerializer,
                             OrderSerializer, ProductSerializer)

# Create your views here.


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "category_id"


class CategoryProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryProductSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = "category_id"


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsClientOrAdmin]
    lookup_url_kwarg = "client_id"

    def post(self, request, *args, **kwargs):
        client_id = self.kwargs.get("client_id")
        if Order.objects.filter(client_id=client_id).exists():
            return Response(
                {
                    "error": "Client already has an order",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
            )
        if client_id:
            request.data["client"] = client_id
        return super().post(request, *args, **kwargs)


class ClientView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAdminUser]


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsClientOrAdmin]
    lookup_url_kwarg = "client_id"

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().destroy(request, *args, **kwargs)


class ClientOrderView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientOrderSerializer
    permission_classes = [IsClientOrAdmin]

    def get_queryset(self):
        client_id = self.kwargs.get("client_id")
        return Order.objects.filter(client_id=client_id)

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)
