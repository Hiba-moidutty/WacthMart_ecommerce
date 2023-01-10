from django.urls import path
from . import views


urlpatterns = [
  path('',views.coupon,name = 'coupon'),
  path('add_coupon',views.add_coupon,name = 'add_coupon'),
  path('delete_coupon',views.delete_coupon,name = 'delete_coupon'),
  path('apply_coupon',views.apply_coupon,name ='apply_coupon'),
]