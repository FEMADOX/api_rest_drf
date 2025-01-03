from django.urls import path

from api_payment.views import StripePaymentView, payment_page

urlpatterns = [
    path(
        'client/<int:client_id>/create-payment/',
        StripePaymentView.as_view(),
        name='create-payment',
        ),
    path(
        'payment/',
        payment_page,
        name='payment_page',
        ),
]
