from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action

from auth_service.permissions import HasScopePermission
from auth_service.scopes import Scopes
from categories.serializers.serializers import CategorySerializer
from categories.services.category_service import CategoryService
from ecommerce_service.common.paginations import CustomPagination
from ecommerce_service.common.success_wrapper import success_response


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    """
    PERMISSIONS
    """
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                HasScopePermission(required_scopes=[Scopes.CATEGORIES_READ])
            ]

        if self.action in ["create", "partial_update", "destroy", "hard_delete"]:
            return [
                HasScopePermission(required_scopes=[Scopes.CATEGORIES_WRITE])
            ]

        return super().get_permissions()

    def get_queryset(self):
        return CategoryService.list_active_categories()


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Categories fetched successfully",
            status_code=status.HTTP_200_OK,
        )
        
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Category fetched successfully",
            status_code=status.HTTP_200_OK,
        )


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.create_category(serializer.validated_data)
        output = self.get_serializer(category)

        return success_response(
            data=output.data,
            message="Category created successfully",
            status_code=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, *args, **kwargs):
        category = self.get_object()

        serializer = self.get_serializer(
            category, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category, serializer.validated_data
        )

        return success_response(
            data=self.get_serializer(category).data,
            message="Category updated successfully",
            status_code=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        CategoryService.soft_delete_category(category)

        return success_response(
            data=None,
            message="Category soft-deleted successfully",
            status_code=status.HTTP_200_OK,
        )


    @action(detail=True, methods=["delete"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        CategoryService.hard_delete_category(pk)

        return success_response(
            data=None,
            message="Category permanently deleted",
            status_code=status.HTTP_200_OK,
        )
