from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['completed', 'target_date']

    def __str__(self):
        return self.name

    def get_progress_percentage(self):
        if self.target_amount > 0:
            return min((self.current_amount / self.target_amount) * 100, 100)
        return 0

    def get_remaining_amount(self):
        return max(self.target_amount - self.current_amount, 0)

    def get_remaining_days(self):
        if self.completed:
            return 0
        today = timezone.now().date()
        if self.target_date < today:
            return 0
        return (self.target_date - today).days

    def get_daily_saving_needed(self):
        remaining_days = self.get_remaining_days()
        if remaining_days > 0:
            return self.get_remaining_amount() / remaining_days
        return 0

    def update_progress(self, amount):
        self.current_amount = min(self.current_amount + amount, self.target_amount)
        if self.current_amount >= self.target_amount:
            self.completed = True
        self.save()
