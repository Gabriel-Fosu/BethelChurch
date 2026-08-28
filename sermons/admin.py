from django.contrib import admin
from .models import Sermon, Series, Speaker

# Register your models here.
@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):

    list_display = ['name', 'title']

    search_fields = ['name']

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):

    list_display = ['title', 'start_date', 'end_date']

    # auto fill slug from title as you type
    prepopulated_fields = {'slug': ('title',)}

    search_fields = ['title']

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'series', 'date', 'is_published']

    # filter sidebar on the right
    list_filter = ['speaker', 'series', 'is_published']

    #search bar at the top
    search_fields = ['title', 'description', 'scripture_reference']

    # auto fill slug from title as you type
    prepopulated_fields = {'slug': ('title',)}

    # click is_published directly in the list without opening the sermon
    list_editable = ['is_published']

    # default sort order in admin
    ordering = ['-date']