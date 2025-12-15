import time
from django.db import models
from products.models import Product
from users.models import User


def generate_order_id():
    return f"ORD{int(time.time() * 1000)}"


class Order(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_SHIPPED = "SHIPPED"
    STATUS_COMPLETED = "COMPLETED"
    

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_SHIPPED,"Shipped"),
        (STATUS_COMPLETED,"Completed")
    ]

    id = models.CharField(
        primary_key=True,
        max_length=30,
        default=generate_order_id,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
