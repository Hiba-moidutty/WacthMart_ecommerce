from django.urls import path,include
from . import views

urlpatterns = [

  #CART 

  path('',views.cart_view,name='cart_view'),
  path('add_to_cart',views.add_to_cart,name='add_to_cart'),
  path('remove_from_cart',views.remove_from_cart,name='remove_from_cart'),
  path('remove_item_cart',views.remove_item_cart,name='remove_item_cart'),
  path('quantity_increase/',views.quantity_increase,name='quantity_increase'),
  #CHECKOUT 
  path('checkout/',views.checkout,name='checkout'),
]