from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.models import User
from auth_service.serializers.login_serializer import LoginSerializer
from auth_service.scopes import ScopeService
from ecommerce_service.common.jwt_utils import (
    generate_access_token,
    generate_refresh_token,
)
from ecommerce_service.common.success_wrapper import success_response


class LoginView(APIView):
    """
    Issues access + refresh JWT with scopes
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        auth=[],
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful"),
            401: OpenApiResponse(description="Invalid credentials"),
            403: OpenApiResponse(description="User inactive"),
        },
        tags=["Authentication"],
        summary="User Login",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower()
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return success_response(
                data=None,
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return success_response(
                data=None,
                message="User account is inactive",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        scopes = ScopeService.scopes_for_role(user.role)

        payload = {
            "user_id": str(user.id),
            "role": user.role,
            "scopes": scopes,
        }

        access_token = generate_access_token(payload)
        refresh_token = generate_refresh_token(payload)

        return success_response(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 1800,
                "scopes": scopes,
            },
            message="Login successful",
            status_code=status.HTTP_200_OK,
        )
