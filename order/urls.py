from django.contrib import admin
from django.urls import path
from . import views
  
urlpatterns =[
  #user side
  path('place_order/',views.place_order,name='place_order'),
  path('order_success/',views.order_success,name='order_success'),
  path('order_cancel/',views.order_cancel,name = 'order_cancel'),
  path('order_details/',views.order_details,name = 'order_details'),



  #Admin side
  path('orderlist/',views.admin_orderlist,name = 'orderlist'),
  path('admin_orderedit/',views.admin_orderedit,name = 'admin_orderedit'),
  path('admin_order_cancel/',views.admin_order_cancel,name = 'admin_order_cancel'),
  path('return_order/',views.return_order,name = 'return_order'),
  path('approve_return/',views.approve_return,name = 'approve_return'),
  path('order_invoice/',views.order_invoice,name = 'order_invoice'),

]