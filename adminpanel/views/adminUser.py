from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def admin_login(request):
    
    
    context={}


    return render(request,"./templateAdmin/login.html",context)

@login_required(login_url='/admin-login/')
def admin_panel_home(request):
    
    context={}


    return render (request,"./templateAdmin/index.html",context)

@login_required(login_url='/admin-login/')
def user_logout(request):
    logout(request)
    return redirect("/home")
