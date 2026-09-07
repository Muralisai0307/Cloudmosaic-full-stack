from rest_framework import generics, status
from rest_framework.response import Response
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer

class JobListAPIView(generics.ListAPIView):
    http_method_names = ['get', 'head', 'options']
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Jobs retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class JobApplicationCreateView(generics.CreateAPIView):
    http_method_names = ['post', 'head', 'options']
    throttle_scope = 'job_application'
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def create(self, request, *args, **kwargs):
        # Frontend multipart form data might pass 'job' as string ID
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Job application submitted successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiTypes

@extend_schema(
    responses={
        200: OpenApiTypes.BINARY,
        404: OpenApiTypes.OBJECT,
    },
    description="Authorized administrator resume download endpoint."
)
class AdminResumeDownloadView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk, *args, **kwargs):
        application = get_object_or_404(JobApplication, pk=pk)
        if not application.resume:
            return HttpResponse("No resume attached.", status=404)
        
        # Nginx internal redirect path
        # In production, Nginx MUST be configured with:
        # location /internal-resumes/ {
        #     internal;
        #     alias /path/to/media/resumes/;
        # }
        
        # Extract just the filename from the resume field
        filename = application.resume.name.split('/')[-1]
        internal_url = f"/internal-resumes/{filename}"
        
        response = HttpResponse()
        response['X-Accel-Redirect'] = internal_url
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        # Nginx will provide Content-Type, or we can leave it empty
        return response
