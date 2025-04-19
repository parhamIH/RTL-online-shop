from django.urls import path
from .views.products import *
from .views.adminUser import * 


urlpatterns = [
    path("home",admin_panel_home),
    path("login",admin_login),
    

]
