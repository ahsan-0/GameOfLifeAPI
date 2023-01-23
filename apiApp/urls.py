from django.urls import path 
from . import views

urlpatterns= [
  path('',views.get_patterns,name='get_patterns')
       ]