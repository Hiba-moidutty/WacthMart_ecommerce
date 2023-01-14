from django import forms
from User_Section.models import Banner
from django.forms import ModelForm


class BannerForm(ModelForm):
  class Meta:
    model = Banner
    fields = ["banner_name" , "image" , "product"]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["banner_name"].widget.attrs.update(
            {"class":"input-group ","placeholder":"Banner Name"}
        )
        self.fields["image"].widget.attrs.update(
            {"class":"input-group "}
        )
        self.fields["product"].widget.attrs.update(
            {"class":"input-group "}
        )
           
