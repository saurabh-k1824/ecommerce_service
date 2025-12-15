import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from auth_service.serializers.refresh_serializer import RefreshTokenSerializer
from users.models import User
from auth_service.scopes import ScopeService
from ecommerce_service.common.jwt_utils import (
    generate_access_token,
    generate_refresh_token,
)
from ecommerce_service.common.success_wrapper import success_response


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        auth=[],
        request=RefreshTokenSerializer,
        responses={
            200: OpenApiResponse(description="Token refreshed"),
            401: OpenApiResponse(description="Invalid refresh token"),
        },
        tags=["Authentication"],
        summary="Refresh Access Token",
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["refresh_token"]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return success_response(
                data=None,
                message="Refresh token expired",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.InvalidTokenError:
            return success_response(
                data=None,
                message="Invalid refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if payload.get("token_type") != "refresh":
            return success_response(
                data=None,
                message="Invalid token type",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        user = User.objects.filter(
            id=payload.get("user_id"),
            is_active=True,
        ).first()

        if not user:
            return success_response(
                data=None,
                message="User inactive or not found",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        scopes = ScopeService.scopes_for_role(user.role)

        new_payload = {
            "user_id": str(user.id),
            "role": user.role,
            "scopes": scopes,
        }

        return success_response(
            data={
                "access_token": generate_access_token(new_payload),
                "refresh_token": generate_refresh_token(new_payload),
                "token_type": "Bearer",
            },
            message="Token refreshed successfully",
            status_code=status.HTTP_200_OK,
        )
