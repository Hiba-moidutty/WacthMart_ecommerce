from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

# Create your models here.

class MyAccountManager(BaseUserManager):
  def create_user(self,first_name,last_name,username,email,phone_number,password = None):
    if not email:
      raise ValueError('User must have a valid email address')
    
    if not username:
      raise ValueError('User must have an username')

    user = self.model(
      email        = self.normalize_email(email),
      username     = username,
      first_name   = first_name,
      last_name    = last_name,
      phone_number = phone_number,
    )
    user.set_password(password)
    user.save(using = self._db)
    return user

  def create_superuser(self,email,username,password,first_name,last_name,phone_number):
    user = self.create_user(
      email         = self.normalize_email(email),
      username      = username,
      password      = password,
      first_name    = first_name,
      last_name     = last_name,
      phone_number  = phone_number,
    )

    user.is_admin     = True
    user.is_active    = True
    user.is_superuser = True
    user.is_staff     =True
    user.save(using = self._db)
    return user


class Account(AbstractBaseUser):
  first_name    = models.CharField(max_length=50)
  last_name     = models.CharField(max_length=50)
  username      = models.CharField(max_length=50,unique=True)
  email         = models.EmailField(max_length=100,unique=True)
  phone_number  = models.CharField(max_length=50)

  # required 
  date_joined   = models.DateTimeField(auto_now_add = True)
  last_login    = models.DateTimeField(auto_now_add = True)
  is_admin      = models.BooleanField(default = False)
  is_staff      = models.BooleanField(default = False)
  is_active     = models.BooleanField(default = True)
  is_superuser  = models.BooleanField(default =False)
  blocked       = models.BooleanField(default=False)

  USERNAME_FIELD  ='email'
  REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']


  objects = MyAccountManager()



  def __str__(self):
    return self.email

  def has_permission(self,permission,obj =None):
    return self.is_admin

  def has_module_permission(self,add_label):
    return True



class Profile(models.Model):
  User = settings.AUTH_USER_MODEL
  user = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='profile')
  otp  = models.CharField(max_length=100, null=True, blank = True)
  uid  = models.UUIDField(default = uuid.uuid4)


class Address(models.Model):
  type          = models.CharField(max_length=20)
  user          = models.ForeignKey(Account,on_delete = models.CASCADE)
  phone         = models.CharField(max_length=15)
  name          = models.CharField(max_length=30)
  address_1     = models.CharField(max_length=100)
  pincode       = models.IntegerField()
  district      = models.CharField(max_length=20)
  state         = models.CharField(max_length=20)
  landmark      = models.CharField(max_length=20,null=True)