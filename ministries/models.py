from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Ministry(models.Model):
    MINISTRY_CHOICES = [
        ('youth',     'Youth Ministry'),
        ('men',       "Men's Ministry"),
        ('women',     "Women's Ministry"),
        ('children',  "Children's Ministry"),
        ('outreach',  'Outreach & Missions'),
    ]

    type = models.CharField(max_length=30, choices=MINISTRY_CHOICES, unique=True)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    icon        = models.CharField(max_length=10, blank=True, help_text='Emoji icon')
    image       = models.ImageField(upload_to='ministries/', blank=True)
    leader      = models.CharField(max_length=150, blank=True)
    order       = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_type_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_type_display()

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Ministries'

class SmallGroup(models.Model):
    TYPE_CHOICES = [
        ('mixed', 'Mixed'),
        ('men', "Men's"),
        ('women', "Women's"),
        ('youth', 'Youth'),
        ('couples', 'Couples'),
        ('seniors', 'Seniors'),
    ]
    DAYS_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    ministry = models.ForeignKey(Ministry, on_delete=models.SET_NULL, null=True, blank=True, related_name='ministries')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    group_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='mixed')
    description = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_groups')
    meeting_day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    meeting_time = models.TimeField()
    location_area = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class GroupInterest(models.Model):
    group = models.ForeignKey(SmallGroup, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} interested in {self.group.name}'