from django.urls import path

from api_payment.views import (ConfirmPaymentView, StripePaymentView,
                               payment_page)

urlpatterns = [
    path(
        'client/<int:client_id>/create-payment/',
        StripePaymentView.as_view(),
        name='create-payment',
        ),
    path(
        'payment_page/',
        payment_page,
        name='payment_page',
        ),
    path(
        'payment/confirm/<str:payment_intent_id>/',
        ConfirmPaymentView.as_view(),
        name='confirm-payment',
        ),
]
