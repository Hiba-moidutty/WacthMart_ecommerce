
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),

    # User Management
    path('admin_userlist/',views.admin_userlist,name='admin_userlist'),
    path('block_user/<int:id>/',views.block_user,name='block_user'),

    # Category Management
    path('admin_category/',views.admin_category,name='admin_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),


    # Sub-Category Management
    path('sub_category/',views.sub_category,name ='sub_category'),
    path('add_subcategory/',views.add_subcategory,name ='add_subcategory'),
    path('edit_subcategory/<int:id>/',views.edit_subcategory,name ='edit_subcategory'),
    path('delete_subcategory/<int:id>/',views.delete_subcategory,name ='delete_subcategory'),


    # Product Management
    path('admin_productlist/',views.admin_productlist,name ='admin_productlist'),
    path('add_product/',views.add_product,name ='add_product'),
    path('edit_product/<int:id>/',views.edit_product,name ='edit_product'),
    path('load_subcategory',views.load_subcategory,name ='load_subcategory'),
    path('delete_product/<int:id>/',views.delete_product,name ='delete_product'),
    
    #Sales Report
    path('sales_report/',views.sales_report,name ='sales_report'),
    path('generateSalesReport/',views.generateSalesReport,name ='generateSalesReport'),
   
]