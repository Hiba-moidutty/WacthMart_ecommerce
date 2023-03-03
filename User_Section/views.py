from django.shortcuts import render,redirect
from User_Section.models import Banner
from category.models import Product,Category, SubCategory
from Coupon.models import Coupon
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q

# Create your views here.
def user_landingpg(request):
  categories =Category.objects.all()
  subcategories = SubCategory.objects.all()
  products =Product.objects.all().filter(is_available = True)
  trending = Product.objects.all().order_by('stock')[2:6]
  banners = Banner.objects.all()
  # coupons = Coupon.objects.all()
  context ={'products': products,
  'banners':banners,
  'categories':categories,
  'subcategories':subcategories,
  'trending':trending,
  }
  return render(request,'user_temp/user_landingpg.html',context)



@never_cache
@login_required(login_url='user_login')
def user_home(request):
  if request.user.is_authenticated:
    if request.user.is_superuser == True:
      return redirect('admin_login')
  categories =Category.objects.all()
  subcategories = SubCategory.objects.all()
  products =Product.objects.all().filter(is_available = True)
  trending = Product.objects.all().order_by('stock')[1:5]
  banners = Banner.objects.all()
  # coupons = Coupon.objects.all()
  print(banners,'kkkkkkkkkkkkkkkkkkkkkkk')
  context ={'products': products,
  'banners':banners,
  'categories':categories,
  'subcategories':subcategories,
  'trending':trending,
  }
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


