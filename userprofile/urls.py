from django.contrib import admin
from django.urls import path
from . import views

  
urlpatterns =[
  path('',views.user_profile,name='user_profile'),
  path('add_address',views.add_address,name='add_address'),
  # path('edit_address/',views.edit_address,name='edit_address'),
  path('delete_address/<int:id>',views.delete_address,name='delete_address'),
  path('address_details/',views.address_details,name = 'address_details'),
  path('change_password/',views.change_password,name = 'change_password'),

  ]