from django.shortcuts import render,redirect
from category.models import Product,Category
from .models import Offer_category, Offer_product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse ,JsonResponse



# Create your views here.

@login_required(login_url='admin_login')
def product_offer(request):
  products = Product.objects.all()
  return render(request,'admin_temp/product_offer.html',{'products':products})


@never_cache
@login_required(login_url='admin_login')
def add_product_offer(request,id):
  if request.POST:
    product = Product.objects.get(id= id)
    print(product,'ooooooo....ooooo')
    offer = Offer_product()
    Discount = request.POST.get('discount')
    print(Discount,'ppppppppppppppppppppppp')
    if Offer_product.objects.filter(product_id = id).exists():
      offer = Offer_product.objects.filter(product_id = id)
      for of in offer:
        of.product = product
        of.discount = Discount
        product.offer = Discount
        product.save()
        of.save()
      return redirect('product_offer')
    offer.discount = Discount
    offer.product = product
    offer.save()
    product.offer = Discount
    product.save()
    return redirect('product_offer')
  product = Product.objects.get(id=id)
  return render(request,'admin_temp/add_product_offer.html',{'product': product})



@login_required(login_url='admin_login')
def delete_product_offer(request):
  id = request.GET.get('id')
  print(id,',,,,,,,,,,,,,,,,,,,,,,,,')
  product = Product.objects.get(id=id)
  product.offer= 0
  product.offer_price = 0
  product.save()
  offer = Offer_product.objects.get(product_id =id)
  offer.discount = 0
  offer.save()
  return JsonResponse({'id': id})



@login_required(login_url='admin_login')
def category_offer(request):
  category = Category.objects.all()
  return render(request,'admin_temp/category_offer.html',{"category": category})



@never_cache
@login_required(login_url='admin_login')
def add_category_offer(request,id):
  if request.POST:
    category = Category.objects.get(id=id)
    Discount = request.POST.get('discount')
    if Offer_category.objects.filter(category = category).exists():
      offer = Offer_category.objects.get(category = category)
      offer.discount = Discount
      category.discount = Discount
      category.save()
      offer.save()
      return redirect('category_offer')  
    else:
      offer = Offer_category()
      offer.category = category
      offer.discount = Discount
      offer.save()
      category.discount = Discount
      category.save()
      return redirect('category_offer') 

  category = Category.objects.get(id=id)
  return render(request,'admin_temp/add_category_offer.html',{'category':category})


@login_required(login_url='admin_login')
def delete_category_offer(request):
  try:
    id = request.GET.get('id')
    category = Category.objects.get(id = id)
    discount = category.discount
    category.save()
    offer = Offer_category.objects.get(category = category)
    offer.discount = 0
    offer.save()
    products = Product.objects.filter(category = category,category_offer = discount)
    for i in products:
      i.category_offer = 0
      i.save()
    
    category.discount = 0
    category.save()
    return JsonResponse({'id':id})

  except:
    return redirect('category_offer')

