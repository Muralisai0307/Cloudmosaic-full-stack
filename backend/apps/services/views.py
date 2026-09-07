from rest_framework import generics, status, views
from rest_framework.response import Response
from django.db import connection
from .models import Service
from .serializers import ServiceSerializer

class ServiceListAPIView(generics.ListAPIView):
    http_method_names = ['get', 'head', 'options']
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Services retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

from drf_spectacular.utils import extend_schema, OpenApiTypes

@extend_schema(
    responses={
        200: OpenApiTypes.OBJECT,
        503: OpenApiTypes.OBJECT,
    },
    description="Active health check verifying application and database connectivity."
)
class HealthCheckView(views.APIView):
    http_method_names = ['get', 'head', 'options']
    
    def get(self, request, *args, **kwargs):
        db_healthy = True
        try:
            connection.ensure_connection()
        except Exception:
            db_healthy = False
            
        status_code = status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "success": db_healthy,
            "message": "Service is healthy." if db_healthy else "Database connectivity check failed.",
            "data": {
                "status": "healthy" if db_healthy else "degraded",
                "database": "connected" if db_healthy else "unavailable"
            }
        }, status=status_code)
