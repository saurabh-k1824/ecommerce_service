from rest_framework import serializers
from orders.models import Order


class AdminOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[
            Order.STATUS_CONFIRMED,
            Order.STATUS_SHIPPED,
            Order.STATUS_COMPLETED,
        ]
    )
