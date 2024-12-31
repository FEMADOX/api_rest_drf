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
        fields = ["product", "quantity", "order_price"]


class OrderSerializer(serializers.ModelSerializer):
    products_order = ProductOrderSerializer(many=True, partial=True)

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
            "total_price",
        ]

    def update(self, instance: Order, validated_data: dict):
        updated_order_data = validated_data.pop('products_order')
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        # Existing Products Id
        existing_products_id = [product_order.product.id
                                for product_order
                                in instance.products_order.all()]

        # New Products Id
        new_products_id = [
            product_data["product"].id
            for product_data
            in updated_order_data
            if product_data["product"].id
            not in existing_products_id
        ]

        # Update products_order
        for product_data in updated_order_data:
            product_id = product_data["product"].id
            if (product_id
                    and product_id in existing_products_id):
                product_order = ProductOrder.objects.get(
                    order=instance,
                    product=product_id,
                )

                product_order.quantity = product_data["quantity"]
                product_order.save()

                if product_order.quantity == 0:
                    product_order.delete()

            if (product_id and product_data["quantity"]
                    and product_id in new_products_id):
                product_order = ProductOrder.objects.create(
                    order=instance,
                    **product_data
                )
                product_order.save()

        return instance
