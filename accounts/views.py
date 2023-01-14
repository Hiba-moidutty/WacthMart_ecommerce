from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth,User

from cart.models import Cart,CartItem
from .models import Account
from cart.views import cart_id
from django.http import HttpResponseRedirect

from accounts.models import Profile
from .forms import RegistrationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from accounts.otp import MessageHandler
import random
# # Create your views here.


@never_cache
def user_signup(request):
  if request.user.is_authenticated:
    return redirect('user_home')
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    phone_number = request.POST['phone_number']
    password = request.POST.get('password')
    password2 = request.POST.get('password1')
    
    if password == password2 :
      print('hiiiiii')
      if not first_name.isalpha():
        messages.error(request,'only letters are to be entered in name!!!')
        return redirect(user_signup)
      
      elif len(phone_number)<10 or len(phone_number) >14 :
        messages.error(request,'Phone Number is not a Valid Number!!!')
        return redirect(user_signup)

      elif Account.objects.filter(email=email).exists() or Account.objects.filter(phone_number = phone_number).exists():
        messages.error(request,'The User is Already Taken')
        return redirect(user_signup)
      
      else:
        otp = 1
        message_handler = MessageHandler(phone_number,otp).send_otp()
        context = {
          'first_name': first_name,
          'last_name': last_name,
          'username' : username,
          'email' : email,
          'phone_number' : phone_number,
          'password' : password
          }
        return render(request,'user_temp/otp.html',context)
    else:
      messages.info(request,"The password is not Matching!!!")
      return redirect('user_signup')
  
  else:
    return render(request,'user_temp/user_signup.html')



@never_cache
def user_login(request):
  if request.user.is_authenticated:
    if request.user.is_superuser:
      return redirect('admin_login')
    return redirect('user_home')
  if request.method =="POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(email=email,password=password)
    if user is not None:
      if user.is_superuser is False:
        try:
          cart= Cart.objects.get(cart_id = cart_id(request))
          
          if CartItem.objects.filter(cart=cart).exists():
            cart_item = CartItem.objects.filter(cart=cart)
            for item in cart_item:
              item.user = user
              if CartItem.objects.filter(product = item.product,user =user, variant_id = item.variant_id).exists():
                item_c = CartItem.objects.get(product = item.product,user =user, variant_id = item.variant_id)
                item_c.quantity += item.quantity
                item_c.save()
              else: 
                item.save()

        except:
          print('entering inside except block','/////////////////')
          pass

        login(request,user)
        messages.success(request,"Authenticated Successfully")
        return redirect('user_home')

      else:
        messages.error(request,"Invalid credentials")
        return redirect('user_login')

    else:
      messages.info(request,'Email or Password is Incorrect')
      return redirect('user_login')
  return render(request,'user_temp/user_login.html')


@never_cache
@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('user_landingpg')



def login_otp(request):
  if request.method == 'POST' :
    phone = request.POST.get('phone_number')
    otp = '123456'
    message_handler = MessageHandler(phone,otp).send_otp()
    return render(request,'user_temp/login_otp_check.html',{'phone':phone})
  return render(request,'user_temp/login_otp.html')



def otp_login_validate(request):
  if request.user.is_authenticated:
    return redirect('user_home')
  if request.method == 'POST' and request.POST['otp']:
    otp1 = int(request.POST['otp'])
    phone = request.POST.get('phone')
    print(phone,'#########################')
    validate = MessageHandler(phone,otp1).validate()
    print("validate===",validate)
    if validate == "approved":
      user = Account.objects.get(phone_number = phone)
      login(request,user)
      return redirect('user_home')
    else:
      messages.info(request,"Wrong OTP")
      return render(request,'user_temp/login_otp_check.html',{'phone': phone})
  return render(request,'user_temp/login_otp.html')



def otp_validate(request):
  if request.method =='POST' and request.POST['otp']:
    otp1 = request.POST.get('otp')
    print(otp1)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username =request.POST['username']
    email = request.POST['email']
    phone_number = request.POST['phone_number']
    password = request.POST.get('password')
    validate = MessageHandler(phone_number,otp1).validate()
    if validate == 'approved':
      user = Account.objects.create_user(email= email,phone_number=phone_number,password = password,first_name = first_name,last_name = last_name, username = username)
      user.save()
      messages.info(request,"Account Created")
      return redirect('user_home')
    else:
      messages.info(request,"Wrong OTP")
      context = {
        'first_name' : first_name,
        'last_name' : last_name,
        'email' : email,
        'phone_number' : phone_number,
        'password'  : password,
        'username'  : username
      }
      return render(request,'user_temp/otp.html',context)

  return render(request,'user_temp/otp.html')
      