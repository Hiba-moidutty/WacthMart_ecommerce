
from django.shortcuts import render,redirect,get_object_or_404
from category.models import Product,Category,SubCategory
from cart.models import Cart,CartItem
from accounts.models import Address
from Variation.models import Variation
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
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
      count = CartItem.objects.filter(user = request.user).count()
      print(count,'sssssssssssssssssssssssss//////')
    else:
        cart = Cart.objects.get(cart_id = cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart,is_active = True)
        #Cart.objects.filter(cart_id = cart_id(request)).exists():
          # print(cart)
          # print(cart,cart_items,'kkkkkkkkkkkkkkkkk')

    if cart_items is not None:
      for cart_item in cart_items:
        c_variant = cart_item.variant_id
        if c_variant != "0" :
          v = Variation.objects.get(variation_id = cart_item.variant_id)
          cart_item.save()
        if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
          total +=(cart_item.product.offer_price * cart_item.quantity)
        else:
          total += (cart_item.product.price * cart_item.quantity)
          print(total,'gggggggaaaaaaaaaaaa')
        quantity += cart_item.quantity
      tax = (2 * total)/100
      grand_total = total + tax
      print(grand_total,'xcxxxxxxxxxxxxxxxxxccccccccc')

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


  
def add_to_cart(request):
  product_id=request.GET.get('id')
  color1=request.GET.get('color')
  # print(product_id,color1,"LLLLLLLLLLLLLLLLL")
  current_user = request.user
  product = Product.objects.get(id=product_id)      #to get the product
  variant = 0
  var_id_ = 0
  if request.GET.get('color'):
    color = request.GET.get('color')
    if color != "0":
      variant = Variation.objects.get(product = product, color = color )
      var_id_ = variant.variation_id

  # if user is authenticated
  if current_user.is_authenticated:
    
    if variant is not 0:
      if CartItem.objects.filter(product = product,user = current_user,variant_id = var_id_).exists():
        cart_item = CartItem.objects.get(product = product,user = current_user,variant_id = var_id_)
        
        # to check whether the stock is less than the quantity adding to cart
        if cart_item.quantity >= product.stock :
          cart_item.quantity = product.stock
          cart_item.save()
          status = True
        else:
          cart_item.quantity += 1       
          cart_item.save()
          status = True
      #create a new cart item
      else:
        cart_item = CartItem.objects.create(
          product = product, quantity = 1, user = current_user, variant_id = variant.variation_id
          )
        cart_item.save()
        print(cart_item,'kkkkkkkkkkkkkkkkk')
        status = False
      return JsonResponse({"status" : status})

    else:  

      if CartItem.objects.filter(product = product,user = current_user,variant_id = 0).exists():
        cart_item = CartItem.objects.get(product = product,user = current_user,variant_id = 0)

        # to check whether the stock is less than the quantity adding to cart
        if cart_item.quantity >= product.stock :
          cart_item.quantity = product.stock
          cart_item.save()
          status = True
        else:
          cart_item.quantity += 1       
          cart_item.save()
          status = True
      #create a new cart item
      else:
        cart_item = CartItem.objects.create(
          product = product, quantity = 1, user = current_user, variant_id = 0
          )
        cart_item.save()
        status = False
      return JsonResponse({"status" : status })


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
    #if user is not authenticate
    try:
      cart = Cart.objects.get(cart_id = cart_id(request))          #get the cart using the car_id present in the session
    
      if variant is not '0':
        if CartItem.objects.filter( product=product, cart=cart, variant_id= var_id_).exists():
            cart_item = CartItem.objects.get(product=product, cart=cart,variant_id = var_id_)
            if cart_item.quantity >= product.stock :
              cart_item.quantity = product.stock
              cart_item.save()
              status = True
            else:
              cart_item.quantity += 1       
              cart_item.save()
              status = True
            return JsonResponse({"status": status})
        else:
            # print('ggggggggggggggggg')
            cart_item = CartItem.objects.create(
            product = product, quantity = 1, cart = cart, variant_id = var_id_
            )
            cart_item.save()
            status = False
            return JsonResponse({"status" : status})
      else:
        if CartItem.objects.filter( product=product, cart=cart, variant_id= 0).exists():
          # print('kkkkkkkkkkkkkkkkkkkkk')
          cart_item = CartItem.objects.get(product=product, cart=cart,variant_id = 0)
          if cart_item.quantity >= product.stock :
            cart_item.quantity = product.stock
            cart_item.save()
            status = True

          else:
            cart_item.quantity += 1       
            cart_item.save()
            status = True
          return JsonResponse({"status" : status })
        else:
          cart_item = CartItem.objects.create(
          product = product, quantity = 1, cart = cart, variant_id = 0
          )
          cart_item.save()
          status = False
          return JsonResponse({"status" : status })
    
    except Cart.DoesNotExist : 
      cart = Cart.objects.create(cart_id = cart_id(request))
      cart.save()
      if variant is not '0':
        cart_item = CartItem.objects.create(product = product, quantity = 1,cart = cart , varient_id = var_id_)
        cart_item.save()
        status =False
        return JsonResponse({"status" : status })
      else:
        cart_item = CartItem.objects.create(product = product, quantity= 1, cart = cart)
        cart_item.save()
        status = False
        return JsonResponse({"status" : status })

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


#Increasing the quantity
def quantity_increase(request):
  total= 0 
  grand_total = 0
  tax=0
  product_id = request.GET.get('id')
  v_id = request.GET.get('v_id')
  print(v_id,product_id,'5555555555555')
  product = Product.objects.get(id=product_id)
  if v_id is not '0':
    variant = Variation.objects.get(product=product,variation_id = v_id)
    v_id = variant.variation_id
  if request.user.is_authenticated:
    if v_id is not '0':
      # print('uuuuuuuuuuuuuuuuuuuuuuuuuu')
      if CartItem.objects.filter(product = product,user = request.user,variant_id = v_id).exists():
        cart_item = CartItem.objects.get(product = product, user = request.user, variant_id= v_id)
        if cart_item.quantity >= product.stock:
          cart_item.quantity = product.stock
          cart_item.save()
        else:
          cart_item.save()
    else:
      # print('iiiiiiiiiiiiiiiiiiiiiiii')
      if CartItem.objects.filter(product = product,user = request.user,variant_id = 0).exists():
        cart_item = CartItem.objects.get(product = product, user = request.user, variant_id= 0)
        if cart_item.quantity >= product.stock:
          cart_item.quantity = product.stock
          cart_item.save() 
        else:
          cart_item.save()
    cart_items = CartItem.objects.filter(
        user = request.user, is_active =True
        ).order_by('-id')

  else:
    #if the user is not authenitcate
    try:
      cart = Cart.objects.get(cart_id = cart_id(request))

    except Cart.DoesNotExist:
      cart = Cart.objects.create(cart_id = cart_id(request))
      cart.save()

    if v_id is not '0':
      if CartItem.objects.filter(product = product, cart = cart ,variant_id = v_id).exists():
        cart_item = CartItem.objects.get(product = product, cart = cart, variant_id= v_id)
        print(cart_item,'kkkkkkkkkkkkkkkkkk')
        if cart_item.quantity >= product.stock:
          cart_item.quantity = product.stock
          cart_item.save()
        else:
          cart_item.save()  
    else:
      print(v_id,'DDDDDDDDDDDDDDDDDD')
      if CartItem.objects.filter(product = product,cart = cart,variant_id = 0).exists():
        cart_item = CartItem.objects.get(product = product, cart = cart, variant_id = 0)
        if cart_item.quantity >= product.stock:
          cart_item.quantity = product.stock
          cart_item.save()
        else:
          cart_item.save()
    cart_items = CartItem.objects.filter(cart = cart,is_active = True)

  if cart_item.quantity :
      quantity = cart_item.quantity + 1
      cart_item.quantity = cart_item.quantity + 1 
      cart_item.save()
      if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
        total +=(cart_item.product.offer_price * cart_item.quantity)
      else:
        total += (cart_item.product.price * cart_item.quantity)
      cart_item.save()
      sub = cart_item.sub_total()
      total=0
      for cart_item in cart_items:
        if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
          total +=(cart_item.product.offer_price * cart_item.quantity)
        else:
          total += (cart_item.product.price * cart_item.quantity)
      print(total,'wwwwwwwwwwwrrrrrrrrrr')
      
      tax = (2 * total)/100
      grand_total = total + tax        
  return JsonResponse({"quantity":quantity,"total":total,"tax":tax,"grand_total":grand_total,"sub": sub})
   


#DECREASING THE QUANTITY OF ITEM IN CART VIEW
def remove_item_cart(request):
  total =0
  tax =0
  grand_total=0
  product_id = request.GET.get('id')
  product = get_object_or_404(Product,id = product_id)
  v_id = request.GET.get('v_id')
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(product = product,user = request.user,variant_id = v_id).exists()
      if v_id is not '0':
        variant = Variation.objects.get(variation_id = v_id)
        v_id = variant.variation_id
        cart_item = CartItem.objects.get(product = product,user = request.user,variant_id = v_id)
      else:
        cart_item = CartItem.objects.get(product = product,user = request.user,variant_id = 0)
      cart_items = CartItem.objects.filter(
        user = request.user, is_active =True
        ).order_by('-id')

    else:
      #if user not authenticated
      cart= Cart.objects.get(cart_id = cart_id(request))
      cart_items = CartItem.objects.filter(product = product,cart = cart, variant_id =v_id).exists()
      if v_id is not '0':
        variant = Variation.objects.get(variation_id = v_id)
        v_id = variant.variation_id
        cart_item = CartItem.objects.get(product = product, cart=cart,variant_id = v_id)
      else:
        cart_item = CartItem.objects.get(product = product,cart=cart,variant_id =0)
      cart_items = CartItem.objects.filter(cart = cart,is_active = True)
      
    
    if cart_item.quantity :
      if cart_item.quantity > 1 :
        quantity = cart_item.quantity - 1
        cart_item.quantity = cart_item.quantity - 1 
        cart_item.save()
        if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
          total +=(cart_item.product.offer_price * cart_item.quantity)
        else:
          total += (cart_item.product.price * cart_item.quantity)
        cart_item.save()
        sub = cart_item.sub_total()
        total=0
        for cart_item in cart_items:
          if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
            total +=(cart_item.product.offer_price * cart_item.quantity)
          else:
            total += (cart_item.product.price * cart_item.quantity)
        tax = (2 * total)/100
        grand_total = total + tax
       

  except:
    pass
  return JsonResponse({"quantity":quantity,"total":total,"tax":tax,"grand_total":grand_total,"sub": sub})


#DELETING THE ITEM FROM THE CART
def remove_from_cart(request):
  product_id = request.GET.get('id')
  v_id = request.GET.get('v_id')
  product = get_object_or_404(Product,id = product_id)
  if request.user.is_authenticated:
    if CartItem.objects.filter(product = product, user = request.user,variant_id = v_id).exists():
      cart_item =CartItem.objects.get(product = product, user = request.user,variant_id = v_id)
  else:
    print(product_id,v_id,'hhhhhhhhhhhhhhh')
    cart = Cart.objects.get(cart_id = cart_id(request))
    cart_item = CartItem.objects.get(product = product, cart = cart,variant_id = v_id)
  cart_item.delete()
  status = True
  return JsonResponse({"status":status})



#checkout
@login_required(login_url = 'user_login')
def checkout(request, total=0, quantity=0, cart_items = None):

  address = Address.objects.filter(user = request.user)
  tax = 0
  grand_total = 0
  try:
    cart_items = CartItem.objects.filter(user = request.user, is_active = True)
    # print(cart_items,'////////////////////////')
    for cart_item in cart_items:
      # if cart_item in cart_items:
        if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
          total += (cart_item.product.offer_price * cart_item.quantity)
        else:
          total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total + tax
    # print(total,grand_total,'////////////////////////////')
    applied = None
    coupon = None
    if 'new_price' in request.session:
      new_price = request.session['new_price']
      coupon = request.session['coupon']

      if new_price is not None:
        grand_total = new_price + tax
        applied = True
      # tax = (2*grand_total)/100
      # grand_total = grand_total + tax

  except:
    pass

  context= {
      'total' : total ,
      'quantity' : quantity ,
      'cart_items' : cart_items,
      'tax' : tax,
      'grand_total' : grand_total,
      'coupon' : coupon,
      'applied':applied,
      'address' : address,
      'order_id':12
    }
  return render(request,'user_temp/checkout.html',context)