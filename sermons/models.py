from django.db import models
from django.utils.text import slugify

# Create your models here.
class Speaker(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='speakers/', blank=True)

    def __str__(self):
        return self.name

class Series(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='series/', blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Series'

class Sermon(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    scripture_reference = models.CharField(max_length=200, blank=True)
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True)
    notes_pdf = models.FileField(upload_to='sermons/notes/', blank=True)
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', blank=True)
    tags = models.CharField(max_length=300, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']