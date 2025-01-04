from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import Category, Client, Order, Product, ProductOrder


class StripePaymentViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client_instance = Client.objects.create(
            name="Test Client",
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            title="Test Product",
            category=self.category,
            price=100.0,
        )
        self.order = Order.objects.create(
            code="ORD123",
            client=self.client_instance,
        )
        self.productorder = ProductOrder.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.url = reverse(
            "create-payment", kwargs={"client_id": self.client_instance.id}
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_create_payment_intent_success(self):
        data = {
            "order_id": self.order.id,
            "client_id": self.client_instance.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("client_secret", response.data)
        self.assertIn("payment_url", response.data)

    def test_create_payment_intent_invalid_order(self):
        data = {
            "order_id": 999,  # Invalid order ID
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_intent_order_not_belong_to_client(self):
        another_client = Client.objects.create(name="Another Client")
        data = {"order_id": self.order.id, "client_id": another_client.id}
        url = reverse(
            "create-payment",
            kwargs={"client_id": another_client.id},
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        self.assertIn(
            "You do not have permission to perform this action.",
            response.data["detail"],
        )

    def test_payment_page(self):
        url = reverse("payment_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "api_payment/index.html")

    def test_successful_payment(self):
        data = {
            "order_id": self.order.id,
            "client_id": self.client_instance.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("client_secret", response.data)
        self.assertIn("payment_url", response.data)

        # Simulate payment confirmation
        # (this would normally be done by the frontend)
        payment_intent_id = response.data["client_secret"].split("_secret")[0]
        confirm_url = reverse(
            "confirm-payment",
            kwargs={"payment_intent_id": payment_intent_id},
        )
        confirm_response = self.client.post(confirm_url, format="json")
        self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)
        self.assertIn("status", confirm_response.data)
        self.assertEqual(confirm_response.data["status"], "succeeded")
