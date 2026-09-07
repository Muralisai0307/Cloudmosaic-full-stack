from django.urls import path
from .views import TestimonialListCreateAPIView

urlpatterns = [
    path('testimonials/', TestimonialListCreateAPIView.as_view(), name='testimonial-list-create'),
]
