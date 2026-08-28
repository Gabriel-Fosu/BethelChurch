from django.contrib import admin
from .models import Ministry, SmallGroup, GroupInterest

# Register your models here.
# Shows small groups inside the ministry page in admin
class SmallGroupInline(admin.TabularInline):
    model  = SmallGroup
    extra  = 0
    fields = ['name', 'meeting_day', 'meeting_time', 'location_area', 'is_active']

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['get_type_display', 'leader', 'order']
    list_editable = ['order']
    readonly_fields = ['slug']
    search_fields = ['type', 'description']
    ordering = ['order']
    inlines = [SmallGroupInline]

@admin.register(SmallGroup)
class SmallGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'meeting_day', 'meeting_time', 'location_area', 'is_active']
    list_filter = ['ministry', 'meeting_day', 'is_active']
    search_fields = ['name', 'description', 'location_area']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

@admin.register(GroupInterest)
class GroupInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'group', 'submitted_at']
    list_filter = ['group']
    search_fields = ['name', 'email']
    readonly_fields = ['submitted_at']