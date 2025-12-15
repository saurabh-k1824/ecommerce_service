from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from auth_service.permissions import HasScopePermission
from auth_service.scopes import Scopes
from products.serializers.serializers import ProductSerializer
from products.services.product_service import ProductService
from ecommerce_service.common.paginations import CustomPagination
from ecommerce_service.common.success_wrapper import success_response


class ProductViewSet(ModelViewSet):
    """
    Product CRUD APIs
    """
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "patch", "delete"]

    filterset_fields = {
        "category": ["exact"],
    }


    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                HasScopePermission(required_scopes=[Scopes.PRODUCTS_READ])
            ]

        if self.action in [
            "create",
            "partial_update",
            "destroy",
            "hard_delete",
        ]:
            return [
                HasScopePermission(required_scopes=[Scopes.PRODUCTS_WRITE])
            ]

        return super().get_permissions()

    def get_queryset(self):
        return ProductService.list_active_products()

 
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Products fetched successfully",
            status_code=status.HTTP_200_OK,
        )


    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Product fetched successfully",
            status_code=status.HTTP_200_OK,
        )


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = ProductService.create_product(
            serializer.validated_data
        )

        return success_response(
            data=self.get_serializer(product).data,
            message="Product created successfully",
            status_code=status.HTTP_201_CREATED,
        )


    def partial_update(self, request, *args, **kwargs):
        product = self.get_object()

        serializer = self.get_serializer(
            product, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        product = ProductService.update_product(
            product, serializer.validated_data
        )

        return success_response(
            data=self.get_serializer(product).data,
            message="Product updated successfully",
            status_code=status.HTTP_200_OK,
        )


    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        ProductService.soft_delete_product(product)

        return success_response(
            data=None,
            message="Product soft-deleted successfully",
            status_code=status.HTTP_200_OK,
        )


    @action(detail=True, methods=["delete"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        ProductService.hard_delete_product(pk)

        return success_response(
            data=None,
            message="Product permanently deleted",
            status_code=status.HTTP_200_OK,
        )
