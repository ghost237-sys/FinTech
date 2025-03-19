from django.contrib import admin
from .models import Goal

# Register your models here.

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'current_amount', 'target_date', 'completed', 'user')
    list_filter = ('completed', 'target_date', 'user')
    search_fields = ('name', 'description')
    date_hierarchy = 'target_date'
