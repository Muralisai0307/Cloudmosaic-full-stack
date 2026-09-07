from django.contrib import admin
from .models import MeetingRequest

@admin.register(MeetingRequest)
class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'date', 'time', 'service', 'created_at')
    search_fields = ('name', 'email', 'company')
    list_filter = ('date', 'service')
    readonly_fields = ('created_at',)
