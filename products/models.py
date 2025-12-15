import time
from django.db import models
from categories.models import Category
import uuid


def generate_product_id():
    return f"PROD{uuid.uuid4().hex[:12].upper()}"


class Product(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=30,
        editable=False,
        default=generate_product_id
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    inventory = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True
    )

    class Meta:
        db_table = 'product'
        indexes = [
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"
