from django.shortcuts import render,redirect
from category.models import Product
from .models import Offer_product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# Create your views here.

@login_required(login_url='admin_login')
def product_offer(request):
  product = Product.objects.all()
  return render(request,'admin_temp/product_offer.html',{'product':product})

@never_cache
@login_required(login_url='admin_login')
def add_product_offer(request,id):
  if request.POST:
    product = Product.objects.get(id = id)
    print(product,'oooooooooo........ooooo')
    offer = Offer_product()
    Discount = request.POST.get('discount')
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



