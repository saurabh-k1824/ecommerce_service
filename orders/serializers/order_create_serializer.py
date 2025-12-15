from rest_framework import serializers
from products.models import Product


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(
            id=value,
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "Invalid or inactive product."
            )
        return value


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)

    def validate(self, attrs):
        if not attrs["items"]:
            raise serializers.ValidationError(
                "Order must contain at least one item."
            )
        return attrs
