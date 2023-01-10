from django.db import models
from accounts.models import Account
from category.models import Product
from Variation.models import Variation

# Create your models here.

class Cart(models.Model):
  cart_id    = models.CharField(max_length = 200,blank =True)
  date_added = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.cart_id

class CartItem(models.Model):
  user         = models.ForeignKey(Account,on_delete = models.CASCADE, null =True)
  product      = models.ForeignKey(Product,on_delete = models.CASCADE)
  cart         = models.ForeignKey(Cart,on_delete = models.CASCADE,null = True)
  variations   = models.ManyToManyField(Variation, blank=True)
  variant_id   = models.CharField(max_length=100,null=True,blank=True,default=0)
  quantity     = models.IntegerField()
  is_active    = models.BooleanField(default = True)


  def sub_total(self):
    if self.product.offer_price is not None and self.product.offer_price is not 0:
      return self.product.offer_price * self.quantity
    else:
      return self.product.price*self.quantity

  def sub_total_c(self,coupon_deducted):
    if self.product.offer_price is not None and self.product.offer_price is not 0:
      if coupon_deducted is not 0:
        return self.product.offer_price *self.quantity - coupon_deducted
      else:
        return self.product.offer_price *self.quantity
    else:
      return self.product.price *self.quantity

  def color_find(self):
    if self.variant_id is not '0':
      variant = Variation.objects.get(variation_id = self.variant_id)
      return variant.color