from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ 
        path("",views.variation,name="variation"),   
        path("add_variation",views.add_variation,name="add_variation"), 

    ]