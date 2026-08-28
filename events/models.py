from django.db import models
from django.utils.text import slugify

# Create your models here.
class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default='#6B1E2C')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Event Categories'

class Event(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=300)
    image = models.ImageField(upload_to='events/', blank=True)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def spots_remaining(self):
        if self.max_attendees:
            return None
        registered = self.registrations.filter(is_confirmed=True).count()
        return max(0, self.max_attendees - registered)

    @property
    def is_full(self):
        if self.max_attendees is None:
            return False
        return self.spots_remaining == 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    attendees = models.PositiveIntegerField(default=1)
    is_confirmed = models.BooleanField(default=True)
    payment_reference = models.CharField(max_length=10, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} — {self.event.title}'