from django.shortcuts import render
from . models import Coupon
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='admin_login')
def coupon(request):
  coupon    = Coupon.objects.all()
  return render(request,'admin_temp/coupon.html',{'coupon' : coupon})

