from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberProfile(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('group_leader', 'Group Leader'),
        ('media_team', 'Media Team'),
        ('pastor', 'Pastor'),
        ('admin', 'Admin'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    membership_date = models.DateField(null=True, blank=True)
    receive_sms = models.BooleanField(default=True)
    receive_newsletter = models.BooleanField(default=True)
    joined_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.role})'