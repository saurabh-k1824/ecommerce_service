from rest_framework import serializers
from categories.models import Category
import re


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "is_active", "created_at"]

    def validate_name(self, value: str) -> str:
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Category name must be at least 3 characters long."
            )

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise serializers.ValidationError(
                "Category name must contain only alphabetic characters and spaces."
            )

        return value.title()

    def validate_description(self, value: str) -> str:
        value = value.strip()

        if value and not re.fullmatch(r"[A-Za-z ,]*", value):
            raise serializers.ValidationError(
                "Description can contain only alphabetic characters, spaces, and commas."
            )

        return value
    
    def validate(self, attrs):
        return attrs
