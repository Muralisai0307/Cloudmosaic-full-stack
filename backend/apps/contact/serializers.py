from rest_framework import serializers
from .models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2, max_length=255)
    email = serializers.EmailField(max_length=255)
    service = serializers.CharField(max_length=100)
    message = serializers.CharField(min_length=10)

    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'email', 'service', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        val = value.strip()
        if len(val) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return val
        
    def validate_email(self, value):
        return value.strip()
        
    def validate_service(self, value):
        val = value.strip()
        if not val:
            raise serializers.ValidationError("Service cannot be empty.")
        return val

    def validate_message(self, value):
        val = value.strip()
        if len(val) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return val
