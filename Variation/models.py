from django.db import models
from category.models import Product
# Create your models here.


class Variation(models.Model):
  product       = models.ForeignKey(Product,on_delete=models.CASCADE) 
  variation_id  = models.CharField(max_length=100,null=True)
  color         = models.CharField(max_length=50,null=True,blank =True)
  quantity      = models.IntegerField(null=True,blank=True,default=0)
  price         = models.IntegerField(null=True)