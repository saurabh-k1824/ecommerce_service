from categories.models import Category
from django.shortcuts import get_object_or_404


class CategoryService:

    @staticmethod
    def list_active_categories():
        return Category.objects.filter(is_active=True)

    @staticmethod
    def create_category(validated_data: dict) -> Category:
        return Category.objects.create(**validated_data)

    @staticmethod
    def update_category(category: Category, validated_data: dict) -> Category:
        for field, value in validated_data.items():
            setattr(category, field, value)

        category.save()
        return category

    @staticmethod
    def soft_delete_category(category: Category) -> None:
        category.is_active = False
        category.save(update_fields=["is_active"])

    @staticmethod
    def hard_delete_category(category_id: str) -> None:
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
