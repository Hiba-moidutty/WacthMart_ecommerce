import uuid
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse 
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from Admin_Section.forms import BannerForm
from User_Section.models import Banner
from accounts.models import Account
from datetime import datetime, timedelta
from django.db.models import Count,Sum,Q,F
from django.utils.text import slugify
from category.models import Category,SubCategory,Product
from category.forms import CategoryForm,SubCategoryForm,ProductForm
from order.models import Order
from . utils import *

# Create your views here.

@never_cache
def admin_login(request):
  if request.method =='POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request,email=email,password=password)
    if user.is_superuser == True:
        login(request,user)
        return redirect('admin_home')
    else:
      messages.info(request,'Username/Email or Password in Incorrect')
      return redirect('admin_login')
  return render(request,'admin_temp/admin_login.html')


@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
  month=0
  if request.user.is_superuser == True:
      total_users = Account.objects.filter(is_active = True).count()
      total_products = Product.objects.filter(is_available = True).count()
      total_orders = Order.objects.filter(status='Delivered').count()
      total_revenue = Order.objects.filter(status='Delivered').aggregate(Sum('total_price'))['total_price__sum']
      # t= total_revenue

      #payment method
      cod_m = Order.objects.filter(payment_method ='cash on delivery').count()
      paypal_m = Order.objects.filter(payment_method = 'Paypal').count()
      razorpay_m = Order.objects.filter(payment_method = 'razorpay').count()
       
      #monthly sales
      today   = datetime.now()
      current = today.strftime("%B %d, %Y")
      dates = Order.objects.filter(order_date__month = today.month).values("order_date__date").annotate(order_items=Count('id')).order_by("order_date__date")
      d = dates.count()
      returns = Order.objects.filter(order_date__month = today.month).values("order_date__date").annotate(return_items=Count('id',filter=Q(status="Cancelled"))).order_by("order_date__date")
      r = returns.count()
      sales   = Order.objects.filter(order_date__month = today.month).values("order_date__date").annotate(sales = Count('id',filter=Q(status ="Delivered")),cancelled=Count('id',filter=Q(status="Cancelled"))).order_by("order_date__date")
      s = sales.count()

      monthly_orders=0
      if request.GET.get('Month') !="0":
        currentmonth = datetime.now().month
        month1 = request.GET.get('Month')
        print(month1,'vvvvvvvvvvvvvvvvvv')
        if month1  is not None and month1 !="0":
          print('hhhhhhhhh')
          month = int(month1)
          monthly_orders = Order.objects.filter(order_date__month=month).count()
      # best_moving = Order.objects.filter(order_date__month = today.year).annotate(moving = Count('product_id')).filter(moving__gt = 2)
      return render(request,"admin_temp/admin_home.html",{
      'current' : current,
      'monthly_orders':monthly_orders,
      'total_users': total_users,
      'total_products': total_products,
      'total_revenue': total_revenue,
      'total_orders' : total_orders,
      'cod_m' : cod_m,
      'paypal_m' : paypal_m,
      'razorpay_m': razorpay_m,
      'sales' : sales,
      'dates' : dates,
      'returns' : returns, 
      'month':str(month),
      'months': ["1","2","3","4","5","6","7","8","9","10","11","12"],
      'r' : r,
      's':s,
      'd':d, })
  return redirect("admin_login")


# def by_month(request):
#   print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
#   #by month
#   monthly_orders=[]
#   if request.GET.get('Month') !="0":
#     currentmonth = datetime.now().month
#     month1 = request.GET.get('Month')
#     print(month1,'vvvvvvvvvvvvvvvvvv')
#     if month1  is not None and month1 !="0":
#       print('hhhhhhhhh')
#       month = int(month1)
#       monthly_orders = Order.objects.filter(order_date__month=month).count()
#       print(monthly_orders,'eeeeeeeeeee')
#       return redirect('admin_home')


@never_cache
def admin_logout(request):
  logout(request)
  return redirect('admin_login')


# User Management
@never_cache
@login_required(login_url='admin_login')
def admin_userlist(request):
  if request.user.is_superuser:
    data = Account.objects.all().order_by('-id')
    page = Paginator(data,4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context ={'data':page}
    return render(request,'admin_temp/admin_userlist.html',context)
  return redirect('admin_login')


def block_user(request,id):
  user=Account.objects.get(id=id)
  if user.blocked:
    user.blocked = False
    user.save()
  else:
    user.blocked=True
    user.save()
  return redirect('admin_userlist')


# Category Mangement

@never_cache
@login_required(login_url='admin_login')
def admin_category(request):
  category_name=Category.objects.all()
  context={'categories':category_name}
  return render(request,'admin_temp/admin_category.html',context)


@never_cache
@login_required(login_url='admin_login')
def add_category(request):
  form = CategoryForm()
  if request.method =='POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('admin_category')
  return render(request,'admin_temp/add_category.html',{'form':form})


@never_cache
@login_required(login_url='admin_login')
def edit_category(request,id):
  cat = Category.objects.get(pk=id)
  form = CategoryForm(request.POST or None,instance = cat)
  if request.method=='POST':
    if form.is_valid():
     form.save()
     return redirect('admin_category')
  return render(request,'admin_temp/edit_category.html',{'form':form})


def delete_category(request,id):
  cat = Category.objects.get(pk=id)
  cat.delete()
  return HttpResponseRedirect(reverse('admin_category'))



# Sub-Category Mangement
@login_required(login_url='admin_login')
def sub_category(request):
  subcategory_name=SubCategory.objects.all()
  page = Paginator(subcategory_name,3)
  page_list = request.GET.get('page')
  page = page.get_page(page_list)
  context={'subcategories': page}
  return render(request,'admin_temp/sub_category.html',context) 


@never_cache
@login_required(login_url='admin_login')
def add_subcategory(request):
  parent_category = Category.objects.all()
  context={
    'categories': parent_category 
  }
  if request.method == 'POST':
    if request.POST.get('select_category') and request.POST.get('subcategory_name'):
      category = request.POST.get('select_category')
      subcategory = request.POST.get('subcategory_name')
      # if SubCategory.objects.filter(subcategory_name=subcategory).exists():
      #   messages.error(request,'Already Exits')
      #   return redirect('sub_category')
      # else:
      sub =SubCategory()
      sub.subcategory_name = subcategory
      sub.slug = slugify(subcategory)
      sub.parent_category_id = category
      sub.save()
      messages.error(request,'SubCategory Created')
      return redirect('sub_category')
    
    else:
      messages.error(request,'Required all Fields!!')
      return redirect('sub_category')
  return render(request,'admin_temp/add_subcategory.html',context)



@never_cache
@login_required(login_url='admin_login')
def edit_subcategory(request,id):
  category = Category.objects.all()
  subcat = SubCategory.objects.get(pk=id)
  if request.method =='POST':
    category = request.POST.get('selectcategory')
    subcategory = request.POST.get('subcategory_name')
    # if SubCategory.objects.filter(subcategory_name = subcategory).exists():
    #   messages.error(request,'Already Exists')
    #   return redirect('sub_category')
    # else:
    subcat.subcategory_name = subcategory
    subcat.slug = slugify(subcategory)
    subcat.parent_category_id = category
    subcat.save()
    messages.success(request,'Sub-Category Created')
    return redirect('sub_category')

  return render(request,'admin_temp/edit_subcategory.html',{
    'categories' : category,
    'subcategories' : subcat,
  })


def load_subcategory(request):
  id=request.GET.get('id')
  subcategory = SubCategory.objects.filter(parent_category_id = id)
  print(subcategory)
  return render(request,'admin_temp/dropdown.html',{'subcategory':subcategory})


def delete_subcategory(request,id):
  subcat = SubCategory.objects.get(pk=id)
  subcat.delete()
  return HttpResponseRedirect(reverse('sub_category'))



# Product Management
@never_cache
@login_required(login_url='admin_login')
def admin_productlist(request):
  if request.user.is_superuser:
    data = Product.objects.all().order_by('-id')
    page = Paginator(data,2)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {'products':page}
    return render(request,'admin_temp/admin_productlist.html',context)
  return redirect('add_product')



@never_cache
@login_required(login_url='admin_login')
def add_product(request):
  if request.user.is_superuser:
    parent_category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    context = {
      'parentcategories':parent_category,
      'subcategory': subcategory
    }
    if request.method == 'POST':
      if request.POST.get('product_name') and request.POST.get('price') and request.POST.get('stock') and request.POST.get('product_description') and request.POST.get('subcategory') and request.POST.get('category') and request.FILES['pro_img1'] and request.FILES['pro_img2'] and request.FILES['pro_img3'] and request.FILES['pro_img4']:
        product_name = request.POST.get('product_name')
        if Product.objects.filter(product_name = product_name).exists():
          messages.error(request,'Product Name Already Exists')
          return redirect('admin_productlist')
        product = Product()
        product.product_name =product_name
        product.slug = slugify(product_name)
        product.product_description = request.POST.get('product_description')
        product.stock = request.POST.get('stock')
        product.price = request.POST.get('price')
        product.subcategory_id= request.POST.get('subcategory')
        product.category_id= request.POST.get('category')

        if 'pro_img1' in request.FILES:
          product.img1 = request.FILES['pro_img1']
        if 'pro_img2' in request.FILES:
          product.img2 = request.FILES['pro_img2']
        if 'pro_img3' in request.FILES:
          product.img3 = request.FILES['pro_img3']
        if 'pro_img4' in request.FILES:
          product.img4 = request.FILES['pro_img4']

        if int(product.stock) <= 0:
          product.is_available = False
        else:
          product.is_available = True
        product.save()
        messages.success(request,"New Product Added.")  
        return redirect('admin_productlist')
      else:
        messages.error(request,'Required all Fields!!')
        return redirect('add_product')
    return render(request,'admin_temp/add_product.html',context)
  else:
     return render(request,'admin_temp/admin_login.html')
  


@never_cache
@login_required(login_url='admin_login')
def edit_product(request,id):
  categories = Category.objects.all()
  product = Product.objects.get(pk=id)
  
  if request.method=='POST':
      if 'product_name' in request.POST:
        product_name = request.POST.get('product_name')
        product.product_name = product_name
        product.slug = slugify(product_name)
          
      if 'product_description' in request.POST:
        product.product_description = request.POST.get('product_description')

      if 'stock' in request.POST:
        product.stock  = request.POST.get('stock')
        
      if 'price' in request.POST:
        product.price = request.POST.get('price')

      if 'subcategory' in request.POST:
        product.subcategory_id = request.POST.get('subcategory')

      if 'category' in request.POST:
        product.category_id = request.POST.get('category')

      if 'pro_img1' in request.FILES:
        product.img1 = request.FILES['pro_img1']
      if 'pro_img2' in request.FILES:
        product.img2 = request.FILES['pro_img2']
      if 'pro_img3' in request.FILES:
        product.img3 = request.FILES['pro_img3']
      if 'pro_img4' in request.FILES:
        product.img4 = request.FILES['pro_img4']

      if int(product.stock) <= 0:
        product.is_available = False
      else:
        product.is_available = True
      product.save()
      messages.success(request,"New Product Added!!")
      return redirect('admin_productlist')

  context = {
    'categories' : categories,
    'product' : product
  }
  return render(request,'admin_temp/edit_product.html',context)



def delete_product(request,id):
  product = Product.objects.get(pk=id)
  product.delete()
  # return redirect('admin_productlist')
  return HttpResponseRedirect(reverse('admin_productlist'))


#Sales Report
@never_cache
@login_required(login_url="admin_login")
def sales_report(request):
  orders = Order.objects.annotate(sub_total =F('product__price')*F('quantity')).order_by("-order_date")
  print(orders,'rrrrrrrrrrrrrrrr')
  if request.GET.get('Month') != "0":
    currentMonth = datetime.now().month
    month1 = request.GET.get('Month')
    if month1 is not None and month1 !="0":
      month = int(month1)
      orders = Order.objects.filter(order_date__month=month).annotate(sub_total =F('product__price')*F('quantity')).order_by("-order_date")
    #   return render(request,"admin_temp/sales_report.html",{
    #   "orders" : orders
    # })
  elif request.GET.get('from_date'):
    from_date  = request.GET.get('from_date')
    print(from_date,'jjjjjjjjjjjjjjjj')
    to_date  = request.GET.get('to_date')
    print(to_date,'iiiiiiii')

    if not from_date or not to_date:
      messages.info(request,"Please fill from and to date")
      return redirect(request.META.get('HTTP_REFERER'))

    todate = datetime.strptime(to_date,"%Y-%m-%d")
    to__date = todate + timedelta(1)
    orders = Order.objects.filter(order_date__range =[from_date,to__date]).annotate(sub_total =F('product__price')*F('quantity')).order_by("-order_date")
  page      = Paginator(orders,5)
  page_list = request.GET.get('page')
  page      = page.get_page(page_list)
  return render(request,"admin_temp/sales_report.html",{
      "orders" :page
    })



def generateSalesReport(request):
  to_date = request.GET.get('date','')
  from_date1 = to_date.split(",")[0]
  to_date1 = to_date.split(",")[1]
  
  if to_date1 is '' or from_date1 is '':
    messages.info(request,"Please fill from and to date to export pdf")
    return redirect(request.META.get('HTTP_REFERER'))
  
  t_date = datetime.strptime(to_date1,"%Y-%m-%d")
  to_date11 = t_date + timedelta(1)

  try:
    orders = Order.objects.filter(order_date__range=[from_date1,to_date11]).annotate(sub_total = F('product__price')*F('quantity')).order_by("-order_date")
    print(orders,'yyyyyyyyyyyyyyyyyyyyyy')
    total_rev = 0
    for i in orders:
      total_rev += i.sub_total
    Report = []

    for i in orders:
      item={
        'Date' : i.order_date,
        'User' : i.user.first_name,
        'Product' : i.product.product_name,
        'Quantity' : i.quantity,
        'Price'  : i.product.price,
        'Revenue' : i.sub_total,
        },
      Report.append(item)

  except:
    return HttpResponse("505 not found")
  print(Report)
  values = {
    'Report':Report,
    'from' : from_date1,
    'to' : to_date1,
    'total_rev' : total_rev,
  }
  format = render_to_pdf('admin_temp/Report_pdf.html', values)
  return HttpResponse(format,content_type = 'application/pdf')


# def GenerateCSV(request):
#   messages.info(request,"something error occured!! ")
#   return redirect(request.META.get('HTTP_REFERER'))




@never_cache
@login_required(login_url='admin_login')
def add_banner(request):
  form = BannerForm()
  if request.method == "POST":
    form = BannerForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect("add_banner")
  banner = Banner.objects.all()
  context = {"form" : form,
  "banner" : banner
  }
  return render(request,"admin_temp/add_banner.html",context)


@never_cache
@login_required(login_url='admin_login')
def remove_banner(request):
  id = request.GET.get('id')
  banner = Banner.objects.get(id = id)
  banner.delete()
  return HttpResponseRedirect(request.META["HTTP_REFERER"])
