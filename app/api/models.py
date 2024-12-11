from cloudinary.models import CloudinaryField  # type:ignore
from django.db import models

# Create your models here.


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    image = CloudinaryField("image", default="")
    category: models.ForeignKey = models.ForeignKey(
        Category,
        related_name="Products",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} - {self.price} - {self.category}"


class Client(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField(max_length=254)
    phone: models.CharField = models.CharField(max_length=10)
    adress: models.TextField = models.TextField()

    def __str__(self):
        return f"{self.name} - email: {self.email} - phone: {self.phone}"


class Order(models.Model):
    code: models.CharField = models.CharField(max_length=50)
    date: models.DateField = models.DateField(auto_now_add=True)
    client: models.ForeignKey = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )


class ProductOrder(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT
    )
    quantity: models.IntegerField = models.IntegerField(default=1)
