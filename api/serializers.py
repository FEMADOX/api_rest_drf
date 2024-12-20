from rest_framework import serializers

from api.models import Category, Client, Order, Product, ProductOrder


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


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
    products_order = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ["code", "client", "products_order"]

    def create(self, validated_data: dict):
        products_order_list = validated_data.pop("products_order")
        order = Order.objects.create(**validated_data)
        [
            ProductOrder.objects.create(order=order, **obj_product_order)
            for obj_product_order in products_order_list
        ]
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    products_order = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ["code", "client", "products_order", "created"]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone",
        ]


class ClientOrderSerializer(serializers.ModelSerializer):
    products_order = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "code",
            "products_order",
        ]
