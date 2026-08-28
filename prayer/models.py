from django.db import models

# Create your models here.
class PrayerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=150, blank=True)
    request = models.TextField()
    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    prayer_count = models.PositiveIntegerField(default=0)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def display_name(self):
        return self.name if self.name else 'Anonymous'

    def __str__(self):
        return f'{self.display_name()} — {self.request[:60]}'

    class Meta:
        ordering = ['-created_at']