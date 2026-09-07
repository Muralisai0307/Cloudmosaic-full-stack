from rest_framework import serializers
from django.utils import timezone
import datetime
from .models import MeetingRequest

class MeetingRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    service = serializers.CharField(max_length=100)
    company = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notes = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    class Meta:
        model = MeetingRequest
        fields = [
            'id', 'service', 'name', 'email', 'phone', 
            'company', 'date', 'time', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        return value.strip()
        
    def validate_company(self, value):
        return value.strip() if value else value
        
    def validate_notes(self, value):
        return value.strip() if value else value

    def validate(self, data):
        date = data.get('date')
        time = data.get('time')
        
        if date and time:
            meeting_datetime = datetime.datetime.combine(date, time)
            # Make the naive datetime timezone-aware according to Django settings
            aware_meeting_datetime = timezone.make_aware(meeting_datetime)
            
            if aware_meeting_datetime < timezone.now():
                raise serializers.ValidationError({
                    "time": "Meeting time cannot be in the past."
                })
                
        return data
