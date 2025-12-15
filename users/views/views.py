from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import User
from users.serializers.serializers import UserSerializer
from ecommerce_service.common.paginations import CustomPagination
from ecommerce_service.common.success_wrapper import success_response


class UserViewSet(ModelViewSet):
    """
    User APIs:
    - Admin: full access
    - User: view/update self only
    """

    serializer_class = UserSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsSelfOrAdmin]

    http_method_names = ["get", "post", "patch", "delete"]



    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return User.objects.filter(is_active=True)

        return User.objects.filter(id=user.id, is_active=True)

 

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="User onboarded successfully",
            status_code=status.HTTP_201_CREATED,
        )


    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)

        response = super().partial_update(request, *args, **kwargs)

        return success_response(
            data=response.data,
            message="User updated successfully",
            status_code=status.HTTP_200_OK,
        )



    def destroy(self, request, *args, **kwargs):
        if request.user.role != "ADMIN":
            return success_response(
                data=None,
                message="Only admin can delete users",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        instance = self.get_object()

        if not instance.is_active:
            return success_response(
                data=None,
                message="User already deactivated",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        instance.is_active = False
        instance.save(update_fields=["is_active"])

        return success_response(
            data=None,
            message="User soft-deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )



    @action(detail=True, methods=["delete"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        if request.user.role != "ADMIN":
            return success_response(
                data=None,
                message="Only admin can hard delete users",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if str(request.user.id) == pk:
            return success_response(
                data=None,
                message="Admin cannot hard delete self",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=pk)
        user.delete()

        return success_response(
            data=None,
            message="User permanently deleted",
            status_code=status.HTTP_204_NO_CONTENT,
        )
