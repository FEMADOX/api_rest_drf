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
        fields = ["id", "product", "quantity"]


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
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance: Order, validated_data: dict):
        updated_order_data = validated_data.pop('products_order')
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        # Update products_order
        existing_product_order_ids = [product_order.id
                                      for product_order
                                      in instance.products_order.all()]
        print(existing_product_order_ids)
        new_product_ids = [
            # ProductOrder.objects.filter(productorder_id)
            product_data["product"].id
            for product_data
            in updated_order_data
            # if product_data["product"]
            # not
            # in instance.products_order.get(product_id=product_data.get(id))
        ]
        print(new_product_ids)

        # Update products_order
        for product_data in updated_order_data:
            product_id = product_data["product"].id
            if (product_id
                    and product_id in existing_product_order_ids):
                print(product_id)
            #     product_order = ProductOrder.objects.get(
            #         id=product_id,
            #         order=instance
            #     )
            #     product_order.product = product_data.get(
            #         'product',
            #         product_order.product
            #     )
            #     product_order.quantity = product_data.get(
            #         'quantity',
            #         product_order.quantity
            #     )
            #     product_order.save()
            # else:
            #     print("ERROR")
        # for product_data in updated_order_data:
        #     product_id = product_data.get('id')
        #     # product_id = instance.id
        #     print(product_id)
        #     if product_id:
        #         product_order = ProductOrder.objects.get(
        #             id=product_id,
        #             order=instance
        #         )
        #         product_order.quantity = product_data.get(
        #             'quantity',
        #             product_order.quantity
        #         )
        #         product_order.save()
        #     else:
        #         print(instance.products_order.all())
        #         print(product_data.keys())
        #         print(updated_order_data)
            #     ProductOrder.objects.create(order=instance,
            #                                 **product_data)

        # Delete products_order not in the request
        # products_order_ids = [
        #     item.get('id')
        #     if item.get('id')
        #     else print(item)
        #     for item in validated_data.all().values("id")
        # ]
        # [
        #     product_order.delete()
        #     for product_order in instance.all()
        #     if product_order.id not in products_order_ids
        # ]
        # products_order_ids = [item.get('id')
        #                       if item.get('id')
        #                       else print(validated_data.get())
        #                       for item in updated_order_data
        #                       ]
        # for product_order in instance.products_order.all():
        #     if product_order.id not in products_order_ids:
        #         product_order.delete()

        # for product_order in instance.products_order.all():
        #     if product_order.id not in product_order_ids:
        #         product_order.delete()

        return instance
