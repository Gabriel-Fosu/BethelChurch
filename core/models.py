from django.db import models

# Create your models here.
class Announcement(models.Model):
    message = models.TextField()
    link = models.URLField(blank=True)
    link_text = models.TextField(max_length=100,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:60]

    class Meta:
        ordering = ['-created_at']

class SiteSettings(models.Model):
    service_times = models.CharField(max_length=200, default='7:00 AM · 9:30AM · 11:00 AM')
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    live_stream_url = models.URLField(blank=True)

    def __str__(self):
        return 'Site Settings'

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

class PlannedVisit(models.Model):
    HEAR_CHOICES = [
        ('friend', 'Friend or Family'),
        ('social', 'Social Media'),
        ('flyer', 'Flyer or Poster'),
        ('walked', 'Walked Past the Church'),
        ('other', 'Other'),
    ]

    #visitor details
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    #visit details
    visit_date = models.DateTimeField(help_text='Which Sunday are you planning to visit?')
    group_size = models.PositiveIntegerField(default=1, help_text='How many people are coming?')
    has_children = models.BooleanField(default=False, help_text='Is there any children?')
    how_heard = models.CharField(max_length=10, choices=HEAR_CHOICES, default='friend')
    questions = models.TextField(blank=True, help_text='Any questions  before you visit?')

    #metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False, help_text='Has the team followed up?')

    def __str__(self):
        return f'{self.name} — {self.visit_date}'

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Planned Visit'
        verbose_name_plural = 'Planned Visits'