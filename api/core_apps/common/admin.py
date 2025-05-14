from django.contrib import admin
from .models import ContentView
from django.contrib.contenttypes.admin import GenericTabularInline
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from typing import Any, Optional

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'viewer_ip', 'last_viewed', 'created_at')
    list_filter = ('content_type', 'last_viewed', 'user', 'viewer_ip')
    date_hierarchy = 'last_viewed'
    readonly_fields = ('user', 'content_object', 'content_type', 'object_id', 'viewer_ip', 'last_viewed', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('content_object', 'content_type', 'object_id')
        }),
        (_('View Details'), {
            'fields': ('user', 'viewer_ip', 'last_viewed')
        }),
        (_('Time Stamps'), {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def has_add_permission(self, request: HttpRequest, obj: Optional[Any] = None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Optional[Any] = None) -> bool:
        return False

class ContentViewInline(GenericTabularInline):
    model = ContentView
    extra = 0
    can_delete = False
    verbose_name = _('Content View')
    verbose_name_plural = _('Content Views')
    readonly_fields = ('user', 'content_object', 'content_type', 'object_id', 'viewer_ip', 'last_viewed', 'created_at', 'updated_at')

    def has_add_permission(self, request: HttpRequest, obj: Optional[Any] = None) -> bool:
        return False
