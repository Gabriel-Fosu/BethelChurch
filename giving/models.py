from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Fund(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Donation(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'one-time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fund = models.ForeignKey(Fund, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=5, default='GHS')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='once')
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)
    paystack_reference = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.donor_name} — GHS {self.amount}'

    class Meta:
        ordering = ['-created_at']