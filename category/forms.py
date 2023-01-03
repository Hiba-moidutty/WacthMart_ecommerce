from django import forms
from django.db.models import fields
from .models import Category,SubCategory,Product

class CategoryForm(forms.ModelForm):

  class Meta:
    model=Category
    fields=['category_name','description']

  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['category_name'].widget.attrs.update({'placeholder':'categoryname'})
    self.fields['description'].widget.attrs.update({'placeholder':'description'})



class SubCategoryForm(forms.ModelForm):

  class Meta:
    model = SubCategory
    fields=['subcategory_name','parent_category']

  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['subcategory_name'].widget.attrs.update({'placeholder':'sub-category name'})  
    self.fields['parent_category'].widget.attrs.update({'placeholder':'category name'})   
 


class ProductForm(forms.ModelForm):

  class Meta:
    model = Product
    fields=['product_name','product_description','price','img1','img2','img3','img4','stock','is_available','category','subcategory']

  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['product_name'].widget.attrs.update({'placeholder':'product name'})  
    self.fields['product_description'].widget.attrs.update({'placeholder':'description'})   
    self.fields['price'].widget.attrs.update({'placeholder':'price'})  
    self.fields['img1'].widget.attrs.update({'placeholder':'add image'})   
    self.fields['img2'].widget.attrs.update({'placeholder':'add image'})  
    self.fields['img3'].widget.attrs.update({'placeholder':'add image'})   
    self.fields['img4'].widget.attrs.update({'placeholder':'add image'}) 
    self.fields['category'].widget.attrs.update({'placeholder':'category name'})
    self.fields['stock'].widget.attrs.update({'placeholder':'available stock'}) 
    self.fields['subcategory'].widget.attrs.update({'placeholder':'subcategory name'})