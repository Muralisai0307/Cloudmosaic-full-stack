from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    readonly_fields = ('created_at',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('job', 'created_at')
    readonly_fields = ('resume', 'created_at')
    # Exclude resume from list_display to prevent sensitive data exposure
