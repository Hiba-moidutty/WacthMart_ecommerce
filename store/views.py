from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from category import forms
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from category.models import Category,SubCategory,Product
from cart.models import Cart,CartItem
from cart.views import cart_id
from category.forms import CategoryForm,SubCategoryForm,ProductForm
# Create your views here.

def store(request,category_slug = None):
  categories = None
  products = None

  if category_slug is not None:
    print('//////////////////////////////////////')
    categories = get_object_or_404(Category,slug = category_slug)
    products = Product.objects.filter(category =categories,is_available =True)
    product_count = products.count()
    print('//////////////////////////////////////',product_count,products)

  else:
    print('//////////////////////////////////////')
    products = Product.objects.all().filter(is_available = True)
    product_count = products.count()
    print('//////////////////////////////////////',product_count,products)

  context = {
    'products' : products,
    'product_count' :product_count,
  }
  return render(request,'user_temp/store.html',context)



def product_details(request,id):
  single_product = Product.objects.get(id=id)
  in_cart = CartItem.objects.filter(cart__cart_id = cart_id(request),product = single_product).exists()
  context = {
    'single_product':single_product,
    'in_cart' : in_cart
  }  
  return render(request,'user_temp/product_details.html',context)

