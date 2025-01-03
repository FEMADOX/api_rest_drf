from rest_framework import serializers

from api.models import Client, Order


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all()
    )
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all()
    )

    def validate(self, data):
        order = data["order_id"]
        client_id = data["client_id"].id

        if order.client_id != client_id:
            raise serializers.ValidationError(
                "Order doesn't belong to the client.",
            )

        return data

    @property
    def total_price(self):
        order = self.validated_data["order_id"]
        return order.total_price

    # return super().validate(attrs)

    # order_id = serializers.PrimaryKeyRelatedField(
    #   queryset=Order.objects.all())

    # amount = Order.objects.get("total_price")
    # amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    # client_id = serializers.IntegerField()
    # total_price = serializers.FloatField()
    # payment_method = serializers.CharField()
