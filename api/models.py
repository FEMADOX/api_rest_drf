from django.db import models

# Create your models here.


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

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
    updated: models.DateTimeField = models.DateTimeField(auto_now=True,
                                                         auto_now_add=False)

    def __str__(self):
        return f"Product: {self.title} | Category: {self.category}"\
            f" | Price: {self.price}"
