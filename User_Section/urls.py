from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_landingpg, name='user_landingpg'),
    path('user_home/',views.user_home,name='user_home'),
   
  
]