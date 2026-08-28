from django.contrib import admin
from .models import Event, EventCategory, EventRegistration

# Register your models here.
class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    fields = ['name', 'email', 'phone', 'attendees', 'registered_at']
    readonly_fields = ['registered_at']

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'location', 'is_published']
    list_filter = ['category', 'is_published', 'is_paid']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    ordering = ('-date',)
    inlines = [EventRegistrationInline]

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'event', 'attendees', 'registered_at']
    list_filter = ['event']
    search_fields = ['name', 'email']
    readonly_fields = ['registered_at']