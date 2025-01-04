import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from api.models import Order
from api.permissions import IsClientOrAdmin
from api_payment.serializers import PaymentSerializer

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_API


class StripePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsClientOrAdmin]
    lookup_url_kwarg = "client_id"

    def perform_create(self, serializer):
        try:
            data = serializer.validated_data
            order_id = data.get("order_id").id
            order = get_object_or_404(
                Order,
                id=order_id,
                client_id=self.kwargs.get("client_id"),
            )
            total_price = order.total_price

            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency="usd",
                payment_method="pm_card_visa",
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never"
                },
            )
            self.client_secret = intent["client_secret"]
        except Exception as e:
            raise ValidationError({"error": str(e)})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["client_secret"] = self.client_secret
        # response.data["total_price"] = self.serializer_class["total_price"]
        response.data["payment_url"] = request.build_absolute_uri(
            "/api/payment/payment/"
        )
        return response


class ConfirmPaymentView(APIView):
    def post(self, request, payment_intent_id):
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            intent.confirm()
            return Response(
                {"status": intent.status},
                status=status.HTTP_200_OK,
            )
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


def payment_page(request):
    return render(request, "api_payment/index.html")
