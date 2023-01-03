from django.urls import path,include
from . import views


urlpatterns = [
  path('user_signup',views.user_signup,name='user_signup'),
  path('otp_validate',views.otp_validate,name='otp_validate'),
  path('login_otp',views.login_otp,name='login_otp'),
  path('otp_login_validate',views.otp_login_validate,name='otp_login_validate'),
  path('login/',views.user_login,name='user_login'),
  path('logout/',views.user_logout,name='user_logout'),
  
]