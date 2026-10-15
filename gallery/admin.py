from django.contrib import admin
from .models import GalleryCategory, GalleryItem


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display   = ['title', 'category', 'type', 'is_featured', 'order', 'created_at']
    list_filter    = ['type', 'category', 'is_featured']
    search_fields  = ['title', 'description']
    list_editable  = ['is_featured', 'order']
    readonly_fields = ['created_at']
    ordering       = ['order', '-created_at']

    fieldsets = [
        ('Basic Info', {
            'fields': ['title', 'category', 'type', 'description', 'date_taken']
        }),
        ('Media', {
            'fields': ['image', 'video_url'],
            'description': 'Upload a photo OR paste a YouTube URL for videos. Not both.'
        }),
        ('Display', {
            'fields': ['is_featured', 'order']
        }),
        ('Metadata', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]