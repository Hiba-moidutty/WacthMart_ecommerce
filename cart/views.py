
from django.shortcuts import render,redirect,get_object_or_404
from category.models import Product,Category,SubCategory
from cart.models import Cart,CartItem
from accounts.models import Address

from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# Cart Management
# for bringing card id(guest id) from session
def cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart



def cart_view(request,total=0,quantity=0,cart_items = None):
  tax =0
  grand_total =0
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(
        user = request.user, is_active =True
        ).order_by('-id')
      print(cart_items)
    else:
      cart = Cart.objects.get(cart_id = cart_id(request))
      cart_items = CartItem.objects.filter(cart = cart,is_active = True)
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    tax = (2 * total)/100
    grand_total = total + tax

  except ObjectDoesNotExist:
    pass

  context = {
    'total' : total,
    'quantity' : quantity,
    'cart_items' : cart_items,
    'tax' : tax,
    'grand_total' : grand_total,
    }
  return render(request,'user_temp/cart.html',context)


  
def add_to_cart(request,product_id):
  current_user = request.user
  product = Product.objects.get(id=product_id)      #to get the product
  # if user is authenticated
  if current_user.is_authenticated:
      if CartItem.objects.filter(product = product,user = current_user).exists():
        # print('mmmmmmmmmmmmmmmmmmmmmmmmmm')
        cart_item = CartItem.objects.get(product = product,user = current_user)
        # print(cart_item,'????????????????????????????')
        cart_item.quantity += 1       
        cart_item.save()
      #create a new cart item
      else:
        cart_item = CartItem.objects.create(
          product = product, quantity = 1, user = current_user
          )
        # cart_item.clear()
        cart_item.save()
        


      return redirect('cart_view')

    # try:
    #   cart_item = CartItem.objects.get(product=product,user = current_user)
    #   cart_item.quantity += 1       
    #   cart_item.save()
    # except CartItem.DoesNotExist:
    #   cart_item = CartItem.objects.create(
    #   product = product,
    #   quantity = 1,
    #   user = current_user,
    #   )
    #   cart_item.save()
    # return redirect('cart_view')

  else:
    #if the user is not authenticate
    try:
      cart = Cart.objects.get(cart_id = cart_id(request))          #get the cart using the car_id present in the session
    except Cart.DoesNotExist : 
      cart = Cart.objects.create(cart_id = cart_id(request))
      cart.save()
    
    if CartItem.objects.filter( product=product, cart=cart).exists():
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1       
        cart_item.save()
        return redirect('cart_view')
    else:
        cart_item = CartItem.objects.create(
        product = product, quantity = 1, cart = cart
        )
        cart_item.save()
        return redirect('cart_view')


    # try:
    #   cart_item = CartItem.objects.get(product=product,cart=cart)
    #   cart_item.quantity += 1       
    #   cart_item.save()
    # except CartItem.DoesNotExist:
    #   cart_item = CartItem.objects.create(
    #     product = product,
    #     quantity = 1,
    #     cart = cart,
    #   )
    #   cart_item.save()
    # return redirect('cart_view')


def remove_item_cart(request,product_id):
  product = get_object_or_404(Product,id = product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product = product,user = request.user)
    else:
       cart= Cart.objects.get(cart_id = cart_id(request))
       cart_item = CartItem.objects.get(product = product,cart = cart)
    if cart_item.quantity > 1 :
      cart_item.quantity = cart_item.quantity - 1 
      cart_item.save()
    else:
     cart_item.delete()
  except:
    pass
  return redirect('cart_view')



def remove_from_cart(request,product_id):
  
  product = get_object_or_404(Product,id = product_id)
  if request.user.is_authenticated:
    cart_item = CartItem.objects.get(product = product, user = request.user)
  else:
    cart = Cart.objects.get(cart_id = cart_id(request))
    cart_item = CartItem.objects.get(product = product, cart = cart)
  cart_item.delete()
  return redirect('cart_view')



#checkout
@login_required(login_url = 'user_login')
def checkout(request, total=0, quantity=0, cart_items = None):

  address = Address.objects.filter(user = request.user)
  # print('111111111111111111111111')
  tax = 0
  grand_total = 0
  try:
    cart_items = CartItem.objects.filter(user = request.user, is_active = True)
    # print(cart_items,'////////////////////////')
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity
    tax = (2* total)/100
    grand_total = total + tax
    # print(total,grand_total,'////////////////////////////')
  except:
    pass

  context= {
      'total' : total ,
      'quantity' : quantity ,
      'cart_items' : cart_items,
      'tax' : tax,
      'grand_total' : grand_total,
    
      'address' : address
    }
  return render(request,'user_temp/checkout.html',context)