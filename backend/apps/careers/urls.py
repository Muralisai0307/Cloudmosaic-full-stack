from django.urls import path
from .views import JobListAPIView, JobApplicationCreateView, AdminResumeDownloadView

urlpatterns = [
    path('careers/jobs/', JobListAPIView.as_view(), name='job-list'),
    path('careers/jobs/apply/', JobApplicationCreateView.as_view(), name='job-apply'),
    path('careers/applications/<uuid:pk>/resume/download/', AdminResumeDownloadView.as_view(), name='resume-download'),
]
