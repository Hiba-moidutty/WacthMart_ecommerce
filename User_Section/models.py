from django.db import models
from category.models import Product

# Create your models here.

class Banner(models.Model):
  banner_name  = models.CharField(max_length=100, null=True)
  image        = models.ImageField(upload_to = 'images/banners',blank = True, null = True)
  product     = models.ForeignKey(Product,on_delete=models.CASCADE)
  is_active    = models.BooleanField(default =True)

 
  