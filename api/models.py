from django.db import models

# Create your models here.


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    title: models.CharField = models.CharField(max_length=100)
    category: models.ForeignKey = models.ForeignKey(
        Category,
        related_name="Products",
        on_delete=models.CASCADE,
    )
    price: models.DecimalField = models.DecimalField(max_digits=10,
                                                     decimal_places=2)
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        height_field=None,
        width_field=None,
        max_length=None,
        default="",
    )
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True, auto_now_add=False
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-updated"]),
        ]

    def __str__(self):
        return (
            f"Product: {self.title} | Category: {self.category}"
            f" | Price: {self.price}"
        )


class Client(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
    )
    phone: models.CharField = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} -  {self.email} - {self.phone}"


class Order(models.Model):
    code: models.CharField = models.CharField(max_length=100)
    client: models.ForeignKey = models.ForeignKey(
        Client,
        related_name="client_order",
        on_delete=models.CASCADE,
    )
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.client.name}"


class ProductOrder(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order,
        related_name="products_order",
        on_delete=models.RESTRICT,
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
    )
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return (
            f"Order: {self.order} - Product: {self.product} - {self.quantity}"
        )
