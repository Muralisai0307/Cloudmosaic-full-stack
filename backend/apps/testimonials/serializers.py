from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='text', min_length=10)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'email', 'title', 'service', 'rating', 'comment', 'image_url', 'is_approved', 'created_at']
        read_only_fields = ['id', 'is_approved', 'created_at']

    def validate_name(self, value):
        return value.strip()
        
    def validate_comment(self, value):
        return value.strip()
        
    def create(self, validated_data):
        # Force is_approved to False for all API submissions
        validated_data['is_approved'] = False
        return super().create(validated_data)
