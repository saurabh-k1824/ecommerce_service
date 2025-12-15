from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

@api_view(["GET"])
def ping(request):
    return HttpResponse(
        {
            "status": "ok",
            "service": "working"
        },
        status=status.HTTP_200_OK
    )


class MetricsView(APIView):
    """
    Prometheus metrics endpoint
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return HttpResponse(
            generate_latest(),
            content_type=CONTENT_TYPE_LATEST,
        )
