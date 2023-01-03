from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from order.models import Order
from .forms import AddressForm
from accounts.models import Address,Account
from django.contrib import messages, auth
from order import views

# import get_object_or_404()
from django.shortcuts import get_object_or_404
# Create your views here.

@login_required(login_url = "user_login")
def add_address(request):
  dest = request.META.get('HTTP_REFERER')
  if request.method == 'POST' :
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address_1 = request.POST.get('address_1')
    pincode = request.POST.get('pincode')
    landmark = request.POST.get('landmark')
    district = request.POST.get('district')
    state = request.POST.get('state')
    user = request.user
    data = Address.objects.create(
       name= name,
       phone = phone,
       address_1 = address_1,
       pincode =pincode,
       landmark =landmark,
       district =district,
       state =state,
       user =user
    )
    data.save()
    messages.success(request,"New address added Succesfully")
    next = PreUrl.url
    return redirect(next)
  else:
      instance = AddressForm()

  context = {'form': instance ,}
  PreUrl(dest)
  return render(request,'user_temp/add_address.html',context)

class PreUrl:
  url = None
  def __init__(self,destination) -> None:
     PreUrl.url = destination


# def edit_address(request):
  # user_profile = Account.objects.get(email = request.user)
  # if request.method =="POST":
  #   if request.POST['name']:
  #     name = request.POST.get('name')
  #     user_profile.name = name
  #     user_profile.save()

  #   if request.POST['phone']:
  #     phone = request.POST.get('phone')
  #     user_profile.phone = phone
  #     user_profile.save()

  #   if request.POST['address_1']:
  #     address_1 = request.POST.get('address_1')
  #     user_profile.address_1 = address_1
  #     user_profile.save()

  #   if request.POST['pincode']:
  #     pincode = request.POST.get('pincode')
  #     user_profile.pincode = pincode
  #     user_profile.save()

  #   if request.POST['landmark']:
  #     landmark = request.POST.get('landmark')
  #     user_profile.landmark = landmark
  #     user_profile.save()

  #   if request.POST['district']:
  #     district = request.POST.get('district')
  #     user_profile.district = district
  #     user_profile.save()

  #   if request.POST['state']:
  #     state = request.POST.get('state')
  #     user_profile.state = state
  #     user_profile.save()
  #   return redirect('user_profile')

  # address = Address.objects.filter(user = request.user)
  # return render(request,'user_temp/edit_address.html',{
  #   "user_profile" : user_profile,
  #   "address" : address
  #   })



def user_profile(request):
    user = request.user
    print(user,'llllllllllllllllllllllllll')
    user_profile = Account.objects.get(email = user.email)
    address = Address.objects.filter(user = user)
    order = Order.objects.filter(user = user)

    # print(user_profile,address,'hellooooooooooooooooooooooooooooooooooooo')
    return render(request,'user_temp/user_profile.html',{
    'user_profile': user_profile,
    'address':address,
    'order' : order
    })


def address_details(request):
  address = Address.objects.filter(user = request.user)
  return render(request,'user_temp/address_details.html',{"address" : address})
    
  
def delete_address(request,id):
  print('fffffffffffffffffffffffff')
  address=get_object_or_404(Address, id = id).delete()
  return redirect('address_details')


def change_password(request):
  if request.method == 'POST':
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    user = Account.objects.get(email = request.user.email)
    print(user,'pppppppppppppp')

    if new_password == confirm_password:
      success = user.check_password(current_password)
      if success:
        user.set_password(new_password)
        user.save()
        login(request,user)
      
        messages.success(request,'Password Changed')
        return redirect('user_profile')
      else:
        messages.error(request,"Your existing password is incorrect")
        return redirect("user_profile")
    else:
      messages.info(request,"Password does not match!!")
      return redirect("user_profile")

  return redirect('user_profile')
