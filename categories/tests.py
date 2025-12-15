from rest_framework import status
from ecommerce_service.tests.base import BaseAPITestCase
from categories.models import Category


class CategoryAPITest(BaseAPITestCase):

    def setUp(self):
        self.admin = self.create_user(role="ADMIN")
        self.authenticate(self.admin)


    def test_list_categories(self):
        Category.objects.create(name="Mobiles")
        Category.objects.create(name="Laptops")

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["result"]), 2)


    def test_create_category(self):
        payload = {
            "name": "Electronics",
            "description": "Electronic items"
        }

        response = self.client.post("/api/categories/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_invalid_category_name(self):
        payload = {
            "name": "123@@@",
            "description": "Invalid name"
        }

        response = self.client.post("/api/categories/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_create_category(self):
        user = self.create_user(role="USER")
        self.authenticate(user)

        response = self.client.post("/api/categories/", {
            "name": "Fashion"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_soft_delete_category(self):
        category = Category.objects.create(name="TVs")

        response = self.client.delete(
            f"/api/categories/{category.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category.refresh_from_db()
        self.assertFalse(category.is_active)

    def test_hard_delete_category(self):
        category = Category.objects.create(name="Furniture")

        response = self.client.delete(
            f"/api/categories/{category.id}/hard-delete/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 0)


    def test_read_only_fields_not_updated(self):
        category = Category.objects.create(name="Watches")

        response = self.client.patch(
            f"/api/categories/{category.id}/",
            {
                "id": "HACKED",
                "is_active": False
            }
        )

        category.refresh_from_db()
        self.assertTrue(category.is_active)
