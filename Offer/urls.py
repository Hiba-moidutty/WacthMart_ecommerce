from django.urls import path
from . import views

urlpatterns = [
  path('product_offer/',views.product_offer,name = 'product_offer'),
  path('add_product_offer/<int:id>/',views.add_product_offer,name = 'add_product_offer'),
  path('delete_product_offer/',views.delete_product_offer,name = 'delete_product_offer'),

  path('category_offer/',views.category_offer,name = 'category_offer'),
  path('add_category_offer/<int:id>/',views.add_category_offer,name = 'add_category_offer'),
  path('delete_category_offer/',views.delete_category_offer,name = 'delete_category_offer'),




]