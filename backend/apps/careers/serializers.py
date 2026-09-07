from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255)
    cover_letter = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    resume = serializers.FileField(write_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'name', 'email', 'resume', 'cover_letter', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def validate_name(self, value):
        return value.strip()
        
    def validate_cover_letter(self, value):
        return value.strip() if value else value

    def validate_job(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Cannot apply to an inactive job.")
        return value

    def validate_resume(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Resume file size cannot exceed 5MB.")
            
        import magic
        import os
        
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf', '.doc', '.docx']
        if ext not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension. Allowed extensions are PDF, DOC, DOCX.")
            
        # Strict binary signature validation using python-magic
        file_header = value.read(2048)
        value.seek(0)
        
        mime = magic.from_buffer(file_header, mime=True)
        valid_mimes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if mime not in valid_mimes:
            raise serializers.ValidationError("Invalid file content type.")
            
        return value

