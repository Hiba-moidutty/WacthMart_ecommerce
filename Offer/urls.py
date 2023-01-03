from django.urls import path
from . import views


urlpatterns = [
  path('product_offer/',views.product_offer,name = 'product_offer'),
  path('add_product_offer/<int:id>/',views.add_product_offer,name = 'add_product_offer'),
]