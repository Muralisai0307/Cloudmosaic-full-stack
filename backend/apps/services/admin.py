from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'display_order', 'created_at')
    list_editable = ('display_order', 'active')
    list_filter = ('active',)
    search_fields = ('title',)
    readonly_fields = ('created_at',)
