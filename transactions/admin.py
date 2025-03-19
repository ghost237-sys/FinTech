from django.contrib import admin
from .models import Transaction, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'category', 'date', 'user')
    list_filter = ('type', 'category', 'date', 'user')
    search_fields = ('description',)
    date_hierarchy = 'date'
