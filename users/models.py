from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """Custom user model for additional fields"""
    currency = models.CharField(max_length=3, default='USD')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.username

    def get_total_income(self):
        return self.transactions.filter(type='income').aggregate(
            total=models.Sum('amount'))['total'] or 0

    def get_total_expenses(self):
        return self.transactions.filter(type='expense').aggregate(
            total=models.Sum('amount'))['total'] or 0

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()
