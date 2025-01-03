import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Category, Client, Order, Product
from api.serializers import (CategoryProductSerializer, CategorySerializer,
                             ClientOrderSerializer, ClientSerializer,
                             OrderSerializer, PaymentSerializer,
                             ProductSerializer)

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_API


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user and request.user.is_staff
        )


class IsClientOrAdmin(BasePermission):
    def has_permission(self, request, view):
        client_id = view.kwargs.get("client_id")
        return bool(
            request.user.is_authenticated
            and (request.user.id == client_id or request.user.is_staff)
        )


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


class StripePaymentView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsClientOrAdmin]

    def post(self, request: Response, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                order_id = data.get("order_id")
                order = get_object_or_404(Order, id=order_id)
                total_price = order.total_price

                intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),
                    currency="usd",
                    payment_method_types=["card"],
                )
                return Response(
                    {
                        "client_secret": intent["client_secret"],
                    }
                )
            except Exception as e:
                return Response(
                    {
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
