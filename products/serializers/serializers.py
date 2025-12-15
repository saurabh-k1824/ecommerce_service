import re
from rest_framework import serializers
from products.models import Product
from categories.models import Category


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer
    - Validates input only
    - Resolves category safely
    """
    category_id = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "inventory",
            "is_active",
            "category",
            "category_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "category",
        ]


    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Product name must be at least 3 characters long."
            )

        if not re.fullmatch(r"[A-Za-z0-9\s\-]+", value):
            raise serializers.ValidationError(
                "Product name can contain only letters, numbers, spaces, and hyphens."
            )

        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Product price must be greater than zero."
            )
        return value

    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Inventory cannot be negative."
            )
        return value


    def validate(self, attrs):
        instance = self.instance

        category_id = attrs.get("category_id")
        if category_id:
            try:
                category = Category.objects.get(
                    id=category_id,
                    is_active=True
                )
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    {"category_id": "Invalid or inactive category."}
                )
        else:
            category = instance.category if instance else None

        if instance:
            incoming_is_active = attrs.get("is_active")
            if incoming_is_active is True and instance.is_active is False:
                raise serializers.ValidationError(
                    {
                        "is_active": (
                            "Reactivating a product via API is not allowed."
                        )
                    }
                )

        name = attrs.get("name") or (instance.name if instance else None)

        if name and category:
            qs = Product.objects.filter(
                name__iexact=name.strip(),
                category=category,
                is_active=True,
            )
            if instance:
                qs = qs.exclude(pk=instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    {
                        "name": (
                            "An active product with this name already "
                            "exists in the selected category."
                        )
                    }
                )

        attrs["category"] = category
        return attrs
