from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'icon', 'description', 'tags', 'features', 'display_order']
        read_only_fields = ['id']
