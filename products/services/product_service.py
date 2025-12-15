from django.shortcuts import get_object_or_404
from products.models import Product


class ProductService:

    @staticmethod
    def list_active_products():
        return Product.objects.filter(
            is_active=True,
            category__is_active=True
        )

    @staticmethod
    def create_product(validated_data: dict) -> Product:
        return Product.objects.create(**validated_data)

    @staticmethod
    def update_product(product: Product, validated_data: dict) -> Product:
        for field, value in validated_data.items():
            setattr(product, field, value)
        product.save()
        return product

    @staticmethod
    def soft_delete_product(product: Product) -> None:
        product.is_active = False
        product.save(update_fields=["is_active"])

    @staticmethod
    def hard_delete_product(product_id: str) -> None:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
