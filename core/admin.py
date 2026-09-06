from django.contrib import admin
from .models import SiteSettings, PlannedVisit, Announcement

# Register your models here.
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(PlannedVisit)
class PlannedVisitAdmin(admin.ModelAdmin):
    list_display   = ['name', 'email', 'visit_date', 'group_size', 'has_children', 'is_contacted', 'submitted_at']
    list_filter    = ['submitted_at', 'has_children', 'is_contacted', 'visit_date']
    search_fields  = ['name', 'email', 'phone']
    list_editable  = ['is_contacted']
    readonly_fields = ['submitted_at']
    ordering       = ['-submitted_at']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_active', 'created_at']
    list_editable = ['is_active']