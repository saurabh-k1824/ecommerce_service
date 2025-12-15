from rest_framework import serializers
from products.models import Product
from django.db import transaction
from orders.models import Order, OrderItem

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
        """
        Validate inventory before creating order
        """
        items = attrs["items"]
        product_ids = [i["product_id"] for i in items]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids,
            is_active=True
        )

        product_map = {p.id: p for p in products}

        for item in items:
            product = product_map.get(item["product_id"])
            if not product:
                raise serializers.ValidationError(
                    "Invalid product in order."
                )

            if product.inventory < item["quantity"]:
                raise serializers.ValidationError(
                    f"Insufficient inventory for {product.name}"
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        items_data = validated_data["items"]

        order = Order.objects.create(user=user)

        total_amount = 0
        products = Product.objects.select_for_update().filter(
            id__in=[i["product_id"] for i in items_data]
        )
        product_map = {p.id: p for p in products}

        for item in items_data:
            product = product_map[item["product_id"]]

            # Deduct inventory
            product.inventory -= item["quantity"]
            product.save(update_fields=["inventory"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price_at_purchase=product.price,
            )

            total_amount += product.price * item["quantity"]

        order.total_amount = total_amount
        order.save(update_fields=["total_amount"])

        return order


class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
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
