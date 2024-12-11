from rest_framework import serializers

from api.models import Category, Client, Order, Product, ProductOrder


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance: Product):
        representation = super().to_representation(instance)
        representation["image"] = instance.image.url
        return representation


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


# Related Tables Serializers


class CategoryProductSerializer(serializers.ModelSerializer):
    Products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "Products"]


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrder
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ["code", "client", "order_products"]

    def create(self, validated_data):
        order_products_list = validated_data.pop("order_products")
        order = Order.objects.create(**validated_data)
        [
            ProductOrder.objects.create(order=order, **obj_product_order)
            for obj_product_order in order_products_list
        ]
        return order
