from django.db import models

from category.models import Category, Product

# Create your models here.

class Offer_product(models.Model):
  product    = models.OneToOneField(Product, on_delete=models.CASCADE)
  discount   = models.IntegerField()
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  validity   = models.BooleanField(default=True)



class Offer_category(models.Model):
  category   = models.OneToOneField(Category,on_delete=models.CASCADE)
  discount   = models.IntegerField()
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)
  validity   = models.BooleanField(default=True)