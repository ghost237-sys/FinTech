from django.contrib import admin
from .models import Budget

# Register your models here.

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'month', 'user')
    list_filter = ('category', 'month', 'user')
    date_hierarchy = 'month'
