from django.urls import path
from . import views

urlpatterns = [
    path('', views.goal_list, name='goal_list'),
    path('add/', views.goal_add, name='goal_add'),
    path('edit/<int:pk>/', views.goal_edit, name='goal_edit'),
    path('delete/<int:pk>/', views.goal_delete, name='goal_delete'),
    path('update-progress/<int:pk>/', views.goal_update_progress, name='goal_update_progress'),
]
