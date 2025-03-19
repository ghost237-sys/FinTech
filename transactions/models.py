from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    color = models.CharField(max_length=7, default='#000000')  # Hex color code

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ['name', 'user']

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    description = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.type})"
