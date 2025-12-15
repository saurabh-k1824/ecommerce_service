from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date

from auth_service.permissions import HasScopePermission
from auth_service.scopes import Scopes
from ecommerce_service.common.paginations import CustomPagination
from orders.models import Order
from orders.serializers.admin_status_serializer import AdminOrderStatusSerializer
from orders.serializers.order_create_serializer import OrderCreateSerializer
from orders.serializers.order_read_serializer import OrderSerializer
from orders.serializers.cancel_serializer import OrderCancelSerializer
from orders.services.order_service import OrderService
from ecommerce_service.common.success_wrapper import success_response


class OrderViewSet(ModelViewSet):
    pagination_class = CustomPagination 
    http_method_names = ["get", "post"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [HasScopePermission(required_scopes=[Scopes.ORDERS_READ])]

        if self.action in ["create", "cancel_order"]:
            return [HasScopePermission(required_scopes=[Scopes.ORDERS_WRITE])]

        if self.action in ["admin_update_status"]:
            return [HasScopePermission(required_scopes=[Scopes.ORDERS_ADMIN])]

        return super().get_permissions()


    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer


    def get_queryset(self):
        request = self.request
        user = request.user

   
        # page = request.query_params.get("page")
        # limit = request.query_params.get("limit")

        # if not page or not limit:
        #     raise ValidationError(
        #         "Both 'page' and 'limit' query parameters are required."
        #     )

        queryset = Order.objects.filter(is_active=True)

 
        if user.role != "ADMIN":
            queryset = queryset.filter(user=user)

   
        status_param = request.query_params.get("status")
        if status_param:
            valid_statuses = {
                Order.STATUS_PENDING,
                Order.STATUS_CONFIRMED,
                Order.STATUS_SHIPPED,
                Order.STATUS_COMPLETED,
                Order.STATUS_CANCELLED,
            }

            if status_param not in valid_statuses:
                raise ValidationError(
                    f"Invalid status '{status_param}'. "
                    f"Allowed values: {', '.join(valid_statuses)}"
                )

            queryset = queryset.filter(status=status_param)


        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            parsed_start = parse_date(start_date)
            if not parsed_start:
                raise ValidationError(
                    "Invalid start_date format. Use YYYY-MM-DD."
                )
            queryset = queryset.filter(created_at__date__gte=parsed_start)

        if end_date:
            parsed_end = parse_date(end_date)
            if not parsed_end:
                raise ValidationError(
                    "Invalid end_date format. Use YYYY-MM-DD."
                )
            queryset = queryset.filter(created_at__date__lte=parsed_end)

        return queryset


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Orders fetched successfully",
            status_code=status.HTTP_200_OK,
        )

 
    def create(self, request, *args, **kwargs):
        if request.user.role == "ADMIN":
            return success_response(
                data=None,
                message="Admins are not allowed to create orders. Orders must be created by normal users.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user,
            items_data=serializer.validated_data["items"],
        )

        return success_response(
            data=OrderSerializer(order).data,
            message="Order created successfully",
            status_code=status.HTTP_201_CREATED,
        )


    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        serializer = OrderCancelSerializer(data={})
        serializer.is_valid(raise_exception=True)

        OrderService.cancel_order(order)

        return success_response(
            data={"order_id": order.id, "status": order.status},
            message="Order cancelled successfully",
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="admin-status")
    def admin_update_status(self, request, pk=None):
        if request.user.role != "ADMIN":
            return success_response(
                data=None,
                message="Only admin can update order status",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object()

        serializer = AdminOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        OrderService.admin_update_status(
            order=order,
            new_status=serializer.validated_data["status"],
        )

        return success_response(
            data={"order_id": order.id, "status": order.status},
            message="Order status updated successfully",
            status_code=status.HTTP_200_OK,
        )
