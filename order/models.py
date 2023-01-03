from django.db import models
from accounts.models import Account,Address
from category.models import Product
# Create your models here.



class Order(models.Model):
  user          = models.ForeignKey(Account,on_delete = models.CASCADE)
  order_number  = models.CharField(max_length=20)
  address       = models.ForeignKey(Address,on_delete = models.CASCADE)
  ordernote     = models.CharField(max_length=50)
  total_price   = models.FloatField(null = False)
  order_date    = models.DateTimeField(auto_now_add = True)
  status        = models.CharField(max_length = 100, default ='Confirmed')
  amount        = models.FloatField(default = 1 )
  payment_method= models.CharField(max_length = 100, default ='cash on delivery')
  created_at    = models.DateTimeField(auto_now_add=True)
  updated_at    = models.DateTimeField(auto_now=True)
  tax           = models.FloatField()
  product       = models.ForeignKey(Product,null = True,on_delete = models.SET_NULL)
  quantity      = models.IntegerField(null = False)
  payment_id    = models.CharField(max_length=500,null = True, blank = True)


  def sub_total(self):
    return self.product.price * self.quantity

  def name(self):
    a = Product.objects.get(id = self.product)
    return a.product_name
