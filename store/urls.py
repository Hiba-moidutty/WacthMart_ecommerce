from django.contrib import admin
from django.urls import path
from . import views
  
urlpatterns =[
  path('',views.store,name='store'),
  path('product_details/<int:id>/',views.product_details,name = 'product_details'),
  path('<category_slug>/',views.store,name ='products_by_category'),
  path('<category_slug>/<sub_category_slug>/',views.store,name ='products_by_subcategory'),
  path('filter_price',views.filter_price,name ='filter_price'),
  
  
]