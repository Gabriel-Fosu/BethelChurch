from django.db import models

# Create your models here.
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Gallery Categories'


class GalleryItem(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    title       = models.CharField(max_length=200)
    category    = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    type        = models.CharField(max_length=5, choices=TYPE_CHOICES, default='photo')
    image       = models.ImageField(upload_to='gallery/photos/', blank=True)
    video_url   = models.URLField(blank=True, help_text='YouTube or Vimeo URL for videos')
    description = models.TextField(blank=True)
    date_taken  = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']