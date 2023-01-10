import random
from django.shortcuts import render,redirect
from accounts.models import Address
from cart.models import CartItem
from category.models import Product
from django.http import JsonResponse
from .models import Order
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# from userprofile.views import user_profile
import datetime
import uuid



# Create your views here.


def place_order(request, total = 0 , quantity = 0,cart_items = None):
  # print("THANK YOU < YOUR ORDER IS PLACED SUCCESSFULLY ")
  current_user = request.user
  if request.user.is_authenticated:
  # if the cart count is less than or equal to zero, then redirect back to store
    cart_items  = CartItem.objects.filter(user = current_user,is_active = True)
    cart_count  = cart_items.count()
    if cart_count <= 0:
      return redirect('store')

      #to decrease the product quantity from stock
  
  
    for item in cart_items:
      product = Product.objects.get(id = item.product.id)
      minus_product = item.quantity
      minus = product.stock - minus_product
      product.stock = minus
      product.save() 
  
  grand_total = 0
  tax = 0
  num = 0
  for cart_item in cart_items:
      num = num + 1
      total += (cart_item.product.price * cart_item.quantity)
      quantity = cart_item.quantity + quantity 

  tax = (2 * total)/100
  grand_total = total + tax
  p_method = request.POST['p_method']
  # print(p_method,'kkkkkkkkkkkkkkkkkkkkk')
  if request.POST and p_method == 'cash on delivery':
    # print('llllllllllllllllllllllllll')
    address_id = request.POST.get('i_id')
    get_address = Address.objects.get(id = address_id)
    
    order_number = str(random.randint(1000,9999))
    if p_method and address_id is not None:
      # print('eeeeeeeeeeeeeeeeee')
      for item in cart_items :
        Order(product = item.product, user = current_user , 
        address = get_address , status = "placed" , amount = item.product.price ,
        quantity = item.quantity , order_number = order_number, total_price = grand_total,
        payment_method = p_method ,tax = tax).save()
        status = True
      return JsonResponse({'status' : status})

  # if request.POST and p_method == 'razorpay':
  #   order_number = request.POST.get('order_number')
  #   payment_id = request.POST.get('payment_id')
  #   address_id = request.POST.get('i_id')
  #   get_address = Address.objects.get(id = address_id)

  #   if p_method is not None:
  #     for item in cart_items:
  #       Order(product = item.product, user = current_user , address = get_address , status = "placed" , amount = item.product.price ,quantity = item.quantity , order_number = order_number, total_price = grand_total, method = p_method ,tax = tax).save()
  #       status = True
  #       return JsonResponse({'status' : status})


  if request.POST and p_method == 'Paypal':
    print('entering paypal view..............................')
    order_number = str(random.randint(1000,9999))
    payment_id = request.POST.get('payment_id')
    address_id = request.POST.get('i_id')
    get_address = Address.objects.get(id = address_id)

    if p_method is not None:
      for item in cart_items:
        Order(product = item.product, user = current_user ,
         address = get_address , status = "placed" , amount = item.product.price ,
         quantity = item.quantity , order_number = order_number, 
         total_price = grand_total, payment_method = p_method ,tax = tax, payment_id = payment_id ).save()
        print(get_address)
        status = True
      return JsonResponse({'status' : status})


    return redirect('order_success')



    
def order_success(request,total =0,quantity = 0,cart_items =None):
  current_user = request.user
  cart_items = CartItem.objects.filter(user = current_user, is_active = True)
  grand_total = 0
  tax = 0
  for cart_item in cart_items:
    total += (cart_item.product.price * cart_item.quantity)
    quantity += cart_item.quantity
  
  tax = (2*total)/100
  grand_total = total + tax
  if grand_total == 0:
    return redirect ('store')

  # to clear the user's cart
  CartItem.objects.filter(user = current_user).delete()
  return render(request,'user_temp/place_order.html',{'user': current_user,
  'grand_total' : grand_total,
  'tax' : tax
  })


def order_cancel(request):
  id = request.GET.get('id')
  order = Order.objects.get(id=id)
  print(order,'wwwwwwwww.................')
  product = Product.objects.get(id = order.product.id)
  # print(product,'ggggggggg>>>>>>>>>>>>>>>>>>>>')
  order.status = "Cancelled"
  product.stock += order.quantity
  product.save()
  order.save()
  return redirect('order_details')


def order_details(request):
  order = Order.objects.filter(user = request.user)
  return render(request,"user_temp/order_details.html",{"order" : order})



#Admin ORDER MANAGEMENT
@login_required(login_url='admin_login')
def admin_orderlist(request):
  orders = Order.objects.all().order_by('-id')
  page = Paginator(orders,5)
  page_list = request.GET.get('page')
  page = page.get_page(page_list)
  return render(request,'admin_temp/orderlist.html',{'orders':page})



@login_required(login_url='admin_login')
def admin_orderedit(request):
  order_id = request.GET.get('oid')
  value = request.GET.get('value')
  order_obj = Order.objects.get(id = order_id)
  order_obj.status = value
  order_obj.save()
  orders = Order.objects.all().order_by('id') 
  return render(request,'admin_temp/orderlist.html',{'orders':orders})


@login_required(login_url='admin_login')
def admin_order_cancel(request):
  id = request.GET.get('id')
  orders = Order.objects.get(id = id)
  product = Product.objects.get(id = orders.product.id)
  print(product,'ggggggggg>>>>>>>>>>>>>>>>>>>>')
  product.stock += orders.quantity
  product.save()
  orders.status = 'Cancelled'
  orders.save()
  orders = Order.objects.all().order_by('id')
  return render(request,'admin_temp/orderlist.html',{'orders' : orders})



@never_cache
def return_order(request):
  print("llllllllllllll")
  id = request.GET.get('id')
  order = Order.objects.get(id=id)
  product = Product.objects.get(id = order.product.id)
  order.status = "Return requested waiting for approval"
  product.save()
  order.save()
  return redirect('admin_orderedit')



@login_required(login_url='admin_login')
def approve_return(request):
  id = request.GET.get('id')
  orders = Order.objects.get(id = id)
  product = Product.objects.get(id= orders.product.id)
  product.stock += orders.quantity
  product.save()
  orders.status = "Return Approved"
  orders.save()
  orders = Order.objects.all().order_by('id')
  return JsonResponse({"id":id})


def order_invoice(request,id):
  orders = Order.objects.filter(order_id = id)
  id_o = id
  return render(request,"order_invoice.html",{
    "orders":orders,
    "id_o" : id_o
    })