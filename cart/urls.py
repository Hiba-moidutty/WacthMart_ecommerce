from django.urls import path,include
from . import views

urlpatterns = [

  #CART 

  path('',views.cart_view,name='cart_view'),
  path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
  path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
  path('remove_item_cart/<int:product_id>/',views.remove_item_cart,name='remove_item_cart'),

  #CHECKOUT 
  path('checkout/',views.checkout,name='checkout'),
]