from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from users.models import User


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        if payload.get("token_type") != "access":
            raise AuthenticationFailed("Invalid access token")

        user = User.objects.filter(
            id=payload.get("user_id"),
            is_active=True
        ).first()

        if not user:
            raise AuthenticationFailed("User not found")

        request.auth = payload
        request.auth_scopes = payload.get("scopes", [])
        request.user_role = payload.get("role")
        return (user, payload)
