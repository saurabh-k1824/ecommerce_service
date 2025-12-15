from rest_framework.test import APITestCase
from users.models import User
from ecommerce_service.common.jwt_utils import generate_access_token
import uuid
import random


class BaseAPITestCase(APITestCase):

    def create_user(self, role="USER"):
        unique_suffix = uuid.uuid4().hex[:6]

        return User.objects.create(
            id=str(uuid.uuid4()),
            email=f"{role.lower()}_{unique_suffix}@test.com",
            contact_number=f"9{random.randint(100000000, 999999999)}",
            password="Test@123",
            role=role,
            is_active=True,
        )

    def authenticate(self, user):
        payload = {
            "user_id": str(user.id),
            "role": user.role,
            "scopes": self._get_scopes(user.role),
        }

        access_token = generate_access_token(payload)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

    def _get_scopes(self, role):
        if role == "ADMIN":
            return [
                "products:read",
                "products:write",
                "categories:read",
                "categories:write",
                "orders:read",
                "orders:write",
                "orders:admin",
                "users:read",
                "users:write",
            ]
        return [
            "products:read",
            "categories:read",
            "orders:read",
            "orders:write",
        ]
