from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status

from users.models import User
from ecommerce_service.common.jwt_utils import decode_access_token


PUBLIC_ENDPOINTS = {
    ("POST", "/api/users/"),
    ("POST", "/api/auth/login/"),
    ("POST", "/api/auth/refresh/"),
    ("POST", "/api/auth/logout/"),
    ("GET", "/api/schema/"),
    ("GET", "/api/swagger/"),
    ("GET", "/metrics/"),
    ("GET","/api/redoc/")
}


class CustomMiddleware(MiddlewareMixin):
    """
    - Extracts JWT from Authorization header
    - Validates token
    - Attaches user, role, scopes to request
    """

    def process_request(self, request):
        try:
            request_path = request.path
            print("1",request_path)
            if (request.method, request_path) in PUBLIC_ENDPOINTS:
                print("okokokokokok")
                return None
            print("okokoko")
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse(
                    {"success": False, "message": "Authorization header missing"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"success": False, "message": "Invalid authorization header"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = auth_header.split(" ")[1]
            
            # print("111",token)
            try:
                payload = decode_access_token(token)
            except Exception as exc:
                return JsonResponse(
                    {"success": False, "message": str(exc)},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            # print("222",payload)
            user_id = payload.get("user_id")
            role = payload.get("role")
            scopes = payload.get("scopes", [])

            if not user_id or not role:
                return JsonResponse(
                    {"success": False, "message": "Invalid token payload"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "User not found or inactive"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            request.user = user
            request.auth_role = role
            request.auth_scopes = scopes

            return None
        except Exception as e:
            
            print("error in middleware",e)
            return None
