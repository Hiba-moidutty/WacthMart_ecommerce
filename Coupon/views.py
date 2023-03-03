import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import Coupon
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='admin_login')
def coupon(request):
  coupon    = Coupon.objects.all()
  return render(request,'admin_temp/add_coupon.html',{'coupon' : coupon})


@login_required(login_url='admin_login')
def add_coupon(request):
  if request.POST:
    if not request.POST.get('coupon_code'):
      messages.error(request,'Coupon code is required')
      return redirect('coupon')
    name       = request.POST.get('coupon_name')
    code       = request.POST.get('coupon_code')
    discount   = request.POST.get('discount')
    validity   = request.POST.get('coupon_validity')
    limit      = request.POST.get('coupon_limit')
    coupon     = Coupon.objects.create(coupon_name = name, coupon_code = code, coupon_limit = limit, validity_upto = validity, discount = discount)
    coupon.save()
    messages.success(request,'Coupon added successfully')
    return redirect('coupon')


def apply_coupon(request):

  if request.POST:
    d   = datetime.datetime.today()
    now = datetime.date(d.year,d.month,d.day)
    
    total = request.POST.get('total')
    print(total,'yyyyyyyyyyyyy')
    total = float(total)
    code  = request.POST.get('coupon_code')
    try:
      coupon = Coupon.objects.get(coupon_code = code)
    except:
      messages.error(request,"Please enter a valid Coupon")
      return redirect(request.META.get('HTTP_REFERER'))
    if coupon.is_active == False:
      messages.error(request,"This coupon is invalid")
      return redirect(request.META.get('HTTP_REFERER'))
    if coupon.validity_upto < now :
      messages.error(request,"Sorry, The coupon is expired")
      return redirect(request.META.get('HTTP_REFERER'))
    if coupon.is_used:
      messages.error(request,"This coupon is already used")
      return redirect(request.META.get('HTTP_REFERER'))
    if code == coupon.coupon_code:
      discount      = coupon.discount
      limit         = coupon.coupon_limit
      limited_price = total - limit
      discounted_price  = total - total*discount/100
      if limited_price > discounted_price :
        new_price = limited_price
      else:
        new_price  = discounted_price
      coupon.is_used = True
      coupon.save()
      request.session['new_price'] = new_price
      request.session['coupon'] = code
      return redirect(request.META.get('HTTP_REFERER'))

  return HttpResponse('True')
  


def delete_coupon(request):
  code    = request.session['coupon']
  coupon  = Coupon.objects.get(coupon_code = code)
  coupon.is_used = False
  coupon.save()
  request.session.pop('coupon',None)
  request.session.pop('new_price',None)
  request.session.modified = True

  return redirect(request.META.get('HTTP_REFERER'))