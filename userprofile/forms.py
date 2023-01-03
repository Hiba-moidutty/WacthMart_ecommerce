from django import forms
from accounts.models import Address

class AddressForm(forms.ModelForm):
  class Meta:
    model=Address
    fields=["user","phone",'name',"address_1",'pincode','district','state','landmark']


    def __init__(self,*args,**kwargs):
      super().__init__(*args,**kwargs)
      for field in self.fields:
        self.fields[field].widget.attrs["class"] = "form__input form__input--2"