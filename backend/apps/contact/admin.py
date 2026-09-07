from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('service',)
    readonly_fields = ('created_at',)
