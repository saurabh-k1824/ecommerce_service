from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views.views import OrderViewSet

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = router.urls
# urlpatterns+=[
# path("orders/<str:order_id>/admin-status/", admin_update_order_status),]
