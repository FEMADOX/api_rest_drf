from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Category, Product

# Create your tests here.


class ProductListViewTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Category Test",
        )
        self.product = Product.objects.create(
            title="Product Test",
            category=self.category,
            price=5,
        )

    def test_should_return_200_status_code(self):
        url = reverse("all_products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_should_create_a_new_product_successfully(self):
    #     url = reverse("all_products")
    #     data = {
    #         "title": "Test Product 2",
    #         "category": self.category.pk,
    #         "price": "5",
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 201)


class ProductDetailViewTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Category Test",
        )
        self.product = Product.objects.create(
            title="Product Test",
            category=self.category,
            price=5,
        )

    def test_should_return_200_status_code(self):
        url = reverse("product_detail", args=["1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse("product_detail", args=["Product Test"])
        self.assertEqual(response.status_code, 200)

    # def test_should_update(self):
    #     url = reverse(
    #         "product_detail",
    #         kwargs={"lookup_value": self.product.pk},
    #     )
    #     data = {
    #         "title": "TEST",
    #         "category": Category.objects.create(name="Category Test 2").pk,
    #         "price": 0,
    #     }
    #     response = self.client.put(url, data, format="json")

    #     self.assertEqual(response.status_code, 200)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.title, data["title"])
    #     self.assertEqual(self.product.category.pk, data["category"])
    #     self.assertEqual(self.product.price, data["price"])

    # def test_should_delete(self):
    #     url = reverse(
    #         "product_detail",
    #         kwargs={"lookup_value": self.product.pk},
    #     )
    #     response = self.client.delete(url)

    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(self.client.get(url).status_code, 404)


class CategoryListViewTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Category Test",
        )
        self.product = Product.objects.create(
            title="Product Test",
            category=self.category,
            price=5,
        )

    def test_should_return_200_status_code(self):
        url = reverse("all_categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_should_create_a_new_category_successfully(self):
    #     url = reverse("all_categories")
    #     data = {
    #         "name": "Test Category 2",
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 201)


class CategoryDetailViewTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Category Test",
        )
        self.product = Product.objects.create(
            title="Product Test",
            category=self.category,
            price=5,
        )

    def test_should_return_200_status_code(self):
        url = reverse("category_detail", args=["1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_should_update(self):
    #     url = reverse(
    #         "category_detail",
    #         args=["1"]
    #     )
    #     data = {
    #         "name": "TEST",
    #     }
    #     response = self.client.put(url, data, format="json")

    #     self.assertEqual(response.status_code, 200)
    #     self.category.refresh_from_db()
    #     self.assertEqual(self.category.name, data["name"])

    # def test_should_delete(self):
    #     url = reverse(
    #         "category_detail",
    #         args=["1"]
    #     )
    #     response = self.client.delete(url)

    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(self.client.get(url).status_code, 404)
