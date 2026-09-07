import uuid
import os
from django.db import models
from django.core.validators import FileExtensionValidator

def resume_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1].lower()
    # Force UUID filename to completely neutralize path traversal attacks
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('resumes', new_filename)

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    resume = models.FileField(
        upload_to=resume_upload_path, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"
