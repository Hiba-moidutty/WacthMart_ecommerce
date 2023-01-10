from django.shortcuts import render,redirect
from . models import Variation
from uuid import uuid4
from category. models import Product
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
@login_required(login_url='admin_login')
def variation(request):
  id      = request.GET.get('id')
  product = Product.objects.get(id = id)
  name    = product.product_name
  variation = Variation.objects.filter(product = product)
  colors = ['Pink','Silver','Red','Black','White','Blue','Green','Brown']

  return render(request,"admin_temp/addvariation.html",{
    'name' : name,
    'id': id,
    'variation' : variation,
    "prod":product,
    "colors":colors
  }) 

@never_cache
@login_required(login_url='admin_login')
def add_variation(request):
  id = request.POST.get('id')
  color = request.POST.get('type')
  quantity = request.POST.get('quantity')
  print(quantity,'lllllllllllllllll')
  product = Product.objects.get(id=id)
  v_id = str(uuid4())[:6]
  variation_id = str(product.product_id)+ v_id
  create = Variation.objects.create(product = product,
  color = color, 
  quantity = quantity,
  variation_id = variation_id)
  create.save()
  variation = Variation.objects.filter(product = product)
  return redirect(request.META.get('HTTP_REFERER'))
  

