from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import IsAdminUser
from apps.services.views import HealthCheckView

class ProtectedSpectacularAPIView(SpectacularAPIView):
    permission_classes = [IsAdminUser]

class ProtectedSpectacularSwaggerView(SpectacularSwaggerView):
    permission_classes = [IsAdminUser]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include('apps.contact.urls')),
    path('api/v1/', include('apps.meetings.urls')),
    path('api/v1/', include('apps.newsletter.urls')),
    path('api/v1/', include('apps.careers.urls')),
    path('api/v1/', include('apps.services.urls')),
    path('api/v1/', include('apps.testimonials.urls')),
    
    # API Documentation (Admin only)
    path('api/schema/', ProtectedSpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', ProtectedSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Health Check
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def api_404(request, exception=None):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Not found.", "errors": {}}, status=404)
    from django.views.defaults import page_not_found
    return page_not_found(request, exception)

def api_500(request):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Internal server error.", "errors": {}}, status=500)
    from django.views.defaults import server_error
    return server_error(request)

handler404 = api_404
handler500 = api_500
