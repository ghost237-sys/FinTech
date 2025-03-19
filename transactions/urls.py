from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.transaction_add, name='transaction_add'),
    path('edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
]
