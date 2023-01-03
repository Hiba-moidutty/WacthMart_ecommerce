from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import Account

class RegistrationForm(UserCreationForm):

  class Meta:
    model=Account
    fields=['username','email','password1','password2','phone_number','first_name','last_name']

  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['first_name'].widget.attrs.update({'placeholder':'First Name'})
    self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
    self.fields['username'].widget.attrs.update({'placeholder':'User Name'})
    self.fields['email'].widget.attrs.update({'placeholder':'Email'})
    self.fields['phone_number'].widget.attrs.update({'placeholder':'Phone Number'})
    self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
    self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})