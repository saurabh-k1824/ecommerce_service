from unittest import TestCase
from rest_framework import status
from categories.models import Category
from ecommerce_service.tests.base import BaseAPITestCase
from orders.services.order_service import OrderService
from products.models import Product
from orders.models import Order
from users.models import User
import uuid

class OrderAPITest(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user("USER")
        self.authenticate(self.user)

        self.category = Category.objects.create(name="Mobiles")
        self.product = Product.objects.create(
            name="iPhone 14",
            price=70000,
            inventory=10,
            category=self.category
        )

    def test_user_can_create_order(self):
        response = self.client.post("/api/orders/", {
            "items": [
                {"product_id": self.product.id, "quantity": 2}
            ]
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.product.refresh_from_db()
        self.assertEqual(self.product.inventory, 8)

    def test_admin_cannot_create_order(self):
        admin = self.create_user("ADMIN")
        self.authenticate(admin)

        response = self.client.post("/api/orders/", {
            "items": [{"product_id": self.product.id, "quantity": 1}]
        }, format="json")

        self.assertEqual(response.status_code, 403)

    def test_cancel_order(self):
        order = Order.objects.create(user=self.user)
        response = self.client.post(f"/api/orders/{order.id}/cancel/")
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_status_filter(self):
        response = self.client.get(
            "/api/orders/?page=1&limit=10&status=INVALID"
        )
        self.assertEqual(response.status_code, 400)

class OrderServiceTest(TestCase):

    def test_invalid_status_transition(self):
        user = User.objects.create(
            id=str(uuid.uuid4()),
            email="user@test.com",
            password="Test@123",
            role="USER",
            is_active=True,
        )

        order = Order.objects.create(user=user)

        with self.assertRaises(Exception):
            OrderService.admin_update_status(
                order,
                Order.STATUS_SHIPPED
            )