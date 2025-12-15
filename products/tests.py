from rest_framework import status
from ecommerce_service.tests.base import BaseAPITestCase
from categories.models import Category
from products.models import Product


class ProductAPITest(BaseAPITestCase):

    def setUp(self):
        # Admin user
        self.admin = self.create_user("ADMIN")
        self.authenticate(self.admin)

        # Category
        self.category = Category.objects.create(
            name="Mobiles",
            description="Mobile phones"
        )

        # Product
        self.product = Product.objects.create(
            name="iPhone 14",
            description="Apple smartphone",
            price=69999,
            inventory=10,
            category=self.category,
        )

   
    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["result"]), 1)

    def test_admin_can_create_product(self):
        payload = {
            "name": "Samsung Galaxy S23",
            "description": "Android phone",
            "price": 79999,
            "inventory": 5,
            "category_id": self.category.id,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_cannot_create_product(self):
        user = self.create_user("USER")
        self.authenticate(user)

        payload = {
            "name": "OnePlus",
            "price": 49999,
            "inventory": 5,
            "category_id": self.category.id,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_duplicate_active_product_not_allowed(self):
        payload = {
            "name": "iPhone 14",
            "price": 70000,
            "inventory": 5,
            "category_id": self.category.id,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_invalid_price(self):
        payload = {
            "name": "Cheap Phone",
            "price": -100,
            "inventory": 5,
            "category_id": self.category.id,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_soft_delete_product(self):
        response = self.client.delete(
            f"/api/products/{self.product.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)


    def test_hard_delete_product(self):
        response = self.client.delete(
            f"/api/products/{self.product.id}/hard-delete/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(
            Product.objects.filter(id=self.product.id).exists()
        )

    def test_filter_products_by_category(self):
        response = self.client.get(
            f"/api/products/?category={self.category.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["result"]), 1)
