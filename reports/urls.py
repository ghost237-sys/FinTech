from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports, name='reports'),
    path('income-expense/', views.income_expense_chart, name='income_expense_chart'),
    path('category-distribution/', views.category_distribution_chart, name='category_distribution_chart'),
    path('monthly-trends/', views.monthly_trends_chart, name='monthly_trends_chart'),
]
