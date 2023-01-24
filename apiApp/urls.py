from django.urls import path 
from . import views

urlpatterns= [
  path('patterns',views.get_patterns, name='get_patterns'),
  path('patterns/<str:id>',views.get_single_pattern, name='get_single_pattern'),
  path('users',views.get_users, name='get_users'),
  ]