from django.urls import path
from .views import MeetingRequestCreateView

urlpatterns = [
    path('meetings/', MeetingRequestCreateView.as_view(), name='meetings-create'),
]
