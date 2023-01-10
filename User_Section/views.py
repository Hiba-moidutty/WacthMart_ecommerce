from django.shortcuts import render,redirect
from category.models import Product,Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q

# Create your views here.
def user_landingpg(request):
  products =Product.objects.all().filter(is_available = True)
  context ={
    'products': products,
    }
  return render(request,'user_temp/user_landingpg.html',context)


@never_cache
@login_required(login_url='user_login')
def user_home(request):
  if request.user.is_authenticated:
    if request.user.is_superuser == True:
      return redirect('admin_login')
  products =Product.objects.all().filter(is_available = True)
  context ={'products': products,}
  return render(request,'user_temp/user_home.html',context)


def search(request):
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if 'keyword' :
      product = Product.objects.order_by('-added_date').filter(Q(product_description__icontains =keyword)|Q(product_name__icontains = keyword))
      product_count = product.count()
  context={
    'products': product,
    'product_count': product_count
  }
  return render(request,'user_temp/store.html', context)


