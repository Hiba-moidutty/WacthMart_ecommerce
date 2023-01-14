from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
  category_name  = models.CharField(max_length=50,unique=True)
  slug           = models.SlugField(max_length =100,unique =True)
  description    = models.TextField(max_length = 255, blank=True)
  # category_image = models.ImageField(upload_to='photos/categories', blank=True)
  discount       = models.IntegerField(null = True, blank=True, default=0)

  def get_url(self):
    return reverse('products_by_category',args=[self.slug])

  def __str__(self):
    return self.category_name

  def save(self, *args, **kwargs):
      self.slug = slugify(self.category_name)
      super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
  subcategory_name   = models.CharField(max_length=50)
  slug               = models.SlugField(max_length=200)
  parent_category    = models.ForeignKey(Category,on_delete = models.CASCADE)

  def get_url(self):
    return reverse('products_by_subcategory',args=[self.parent_category.slug,self.slug]) 

  def __str__(self):
    return self.subcategory_name

  # def save(self, *args, **kwargs):
  #   self.slug = slugify(self.subcategory_name)
  #   super(SubCategory, self).save(*args, **kwargs)



class Product(models.Model):
  product_name         = models.CharField(max_length=500,unique=True)
  slug                 = models.SlugField(max_length=200,unique=True)
  product_description  = models.TextField()
  price                = models.FloatField()
  img1                 = models.ImageField(upload_to='images/product_images',blank=True)
  img2                 = models.ImageField(upload_to='images/product_images',blank=True)
  img3                 = models.ImageField(upload_to='images/product_images',blank=True)
  img4                 = models.ImageField(upload_to='images/product_images',blank=True)
  added_date           = models.DateTimeField(auto_now_add=True)
  stock                = models.BigIntegerField()
  is_available         = models.BooleanField(default=False)
  category             = models.ForeignKey(Category,on_delete=models.CASCADE)
  subcategory          = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
  offer                = models.IntegerField(null=True ,blank=True ,default=0)
  category_offer       = models.IntegerField(null=True ,blank=True ,default=0)
  offer_price          = models.IntegerField(null=True ,blank=True ,default=0)
  product_id           = models.CharField(max_length=100 ,null= True ,blank=True, default=0)


  def get_url(self):
    return reverse('product_details',args =[self.category.slug,self.subcategory.slug,self.slug])

  def __str__(self):
    return self.product_name

  # def save(self, *args, **kwargs):
  #   self.slug = slugify(self.product_name)
  #   super(Product, self).save(*args, **kwargs)

  