from django.db import models
from django.conf import settings
from transactions.models import Category

# Create your models here.

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category', 'month']
        ordering = ['-month']

    def __str__(self):
        return f"{self.category.name} - {self.month.strftime('%B %Y')}"

    def get_spent_amount(self):
        month_start = self.month.replace(day=1)
        if self.month.month == 12:
            month_end = self.month.replace(year=self.month.year + 1, month=1, day=1)
        else:
            month_end = self.month.replace(month=self.month.month + 1, day=1)

        return self.category.transaction_set.filter(
            date__gte=month_start,
            date__lt=month_end
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    def get_remaining_amount(self):
        return self.amount - self.get_spent_amount()

    def get_progress_percentage(self):
        spent = self.get_spent_amount()
        if self.amount > 0:
            return min((spent / self.amount) * 100, 100)
        return 0
