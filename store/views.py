from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from Variation.models import Variation
from category import forms
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from category.models import Category,SubCategory,Product
from cart.models import Cart,CartItem
from cart.views import cart_id
from django.db.models import Q
from django.core.paginator import Paginator
# from category.forms import CategoryForm,SubCategoryForm,ProductForm
# Create your views here.

def store(request,category_slug = None,sub_category_slug=None):
  category = Category.objects.all()
  sub_category = SubCategory.objects.all()
  subcategories = None
  categories = None
  products = None
  product = Product.objects.all().filter(is_available = True)
  for i in product:
        if i.category.discount<i.offer:
         if i.offer is not None and i.offer is not 0 :
            i.offer_price = int(i.price - i.price * i.offer/100)
            i.save()
            continue
        if i.category.discount is not None:
            i.category_offer = i.category.discount
            if i.category.discount is not 0:
                i.offer_price = int(i.price - i.price * i.category.discount/100)
            else:
                 i.offer_price = i.category.discount
            i.save()
  if category_slug is not None:
    categories = get_object_or_404(Category,slug = category_slug)
    products = Product.objects.filter(category =categories,is_available =True)
    product_count = products.count()
    paginator=Paginator(products,1)
    page=request.GET.get('page')
    data=paginator.get_page(page)
  
  elif category_slug and sub_category_slug is not None :
    subcategories = get_object_or_404(SubCategory,slug = sub_category_slug)
    products = Product.objects.filter(subcategory = subcategories,category = category_slug)
    product_count = products.count()
    paginator=Paginator(products,1)
    page=request.GET.get('page')
    data=paginator.get_page(page)

  else:
    products = Product.objects.all()
    paginator=Paginator(products,3 )
    page=request.GET.get('page')
    data=paginator.get_page(page)
    product_count = products.count()
    # print('9999999999999999',product_count,products)

  context = {
    'products' : data,
    'category' : category,
    'sub_category' : sub_category,
    'product_count' :product_count,
  }
  return render(request,'user_temp/store.html',context)



def product_details(request,id):
  single_product = Product.objects.get(id=id)
  in_cart = CartItem.objects.filter(cart__cart_id = cart_id(request),product = single_product).exists()
  variation = Variation.objects.filter(product = single_product)
  print(variation,'oooooooooooo')
  context = {
    'single_product':single_product,
    'in_cart' : in_cart,
    "variation":variation
  }  
  return render(request,'user_temp/product_details.html',context)


def filter_price(request):
  category = Category.objects.all()
  selected = request.GET.get('gridradio')
  if int(selected) == 1:
    products = Product.objects.filter(Q(price__lte = 1000))
  elif int(selected) == 2:
    products = Product.objects.filter(Q(price__gte = 1000 , price__lte = 3000))
  elif int(selected) == 3:
    products = Product.objects.filter(Q(price__gte = 3000 , price__lte = 6000))
  elif int(selected) == 5:
    products = Product.objects.filter(Q(price__gte = 6000 , price__lte = 9000))
  elif int(selected) == 6:
    products = Product.objects.filter(Q(price__gte = 9000 , price__lte = 12000))
  else:
    products = Product.objects.filter(Q(price__gte = 12000))

  return render(request,'user_temp/store.html',{
    'products' : products,
    'category': category,
  })


def filter_cat(request):
  category = Category.objects.all()
  selected = request.GET.get('category')
  if int(selected) == 1:
    products = Category.objects.filter(category__category_name ="For ALL")
  elif int(selected) == 2:
    products = Category.objects.filter(category__category_name ="Female Category")
  elif int(selected) == 3:
    products = Category.objects.filter(category__category_name ="Kids Category")
  else:
    products = Category.objects.filter(category__category_name ="Male Category")

  return render(request,'user_temp/store.html',{
    'products' : products,
    'category': category,
  })