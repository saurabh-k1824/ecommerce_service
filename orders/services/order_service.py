from django.db import transaction
from rest_framework.exceptions import ValidationError

from orders.models import Order, OrderItem
from products.models import Product


class OrderService:
    """
    Centralized order business logic
    """

   
    @staticmethod
    @transaction.atomic
    def create_order(user, items_data: list) -> Order:
        product_ids = [i["product_id"] for i in items_data]

        products = Product.objects.select_for_update().filter(
            id__in=product_ids,
            is_active=True
        )

        product_map = {p.id: p for p in products}

        # Inventory validation
        for item in items_data:
            product = product_map.get(item["product_id"])
            if not product:
                raise ValidationError("Invalid product in order.")

            if product.inventory < item["quantity"]:
                raise ValidationError(
                    f"Insufficient inventory for {product.name}"
                )

        order = Order.objects.create(user=user)
        total_amount = 0

        for item in items_data:
            product = product_map[item["product_id"]]

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

    @staticmethod
    @transaction.atomic
    def cancel_order(order: Order):
        if order.status == Order.STATUS_CANCELLED:
            raise ValidationError("Order already cancelled")

        if order.status == Order.STATUS_COMPLETED:
            raise ValidationError("Completed orders cannot be cancelled")

        for item in order.items.select_related("product"):
            product = item.product
            product.inventory += item.quantity
            product.save(update_fields=["inventory"])

        order.status = Order.STATUS_CANCELLED
        order.save(update_fields=["status"])

    @staticmethod
    def admin_update_status(order: Order, new_status: str):
        if order.status == Order.STATUS_CANCELLED:
            raise ValidationError("Cannot update a cancelled order")

        if order.status == Order.STATUS_COMPLETED:
            raise ValidationError("Completed order status cannot be changed")

        allowed_transitions = {
            Order.STATUS_PENDING: [
                Order.STATUS_CONFIRMED,
                Order.STATUS_CANCELLED,
            ],
            Order.STATUS_CONFIRMED: [
                Order.STATUS_SHIPPED,
                Order.STATUS_CANCELLED,
            ],
            Order.STATUS_SHIPPED: [
                Order.STATUS_COMPLETED,
            ],
        }

        if new_status not in allowed_transitions.get(order.status, []):
            raise ValidationError(
                f"Invalid status transition from {order.status} to {new_status}"
            )

        order.status = new_status
        order.save(update_fields=["status"])
