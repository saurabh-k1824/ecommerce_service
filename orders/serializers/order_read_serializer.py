from rest_framework import serializers
from orders.models import Order, OrderItem


class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "product_name",
            "quantity",
            "price_at_purchase",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "items",
            "created_at",
        ]
