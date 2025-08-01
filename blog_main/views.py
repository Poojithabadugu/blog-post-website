from django.shortcuts import render,redirect
from blogs.models import Category,Blogs
from . forms import RegistrationForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def home(request):
    categories =Category.objects.all()
    featured_post=Blogs.objects.filter(is_featcherd=True,status='published')
    posts=Blogs.objects.filter(is_featcherd=False,status='published')
    #print(post)
    context={
        'categories':categories,
        'featured_post':featured_post,
        'posts':posts
    }
    return render(request,'home.html',context)

def register(request):
    if request.method=="POST":
        form =RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form=RegistrationForm()
    context={
        'form':form
    }
    return render(request,'register.html',context)

def login(request):
    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request, "Login successful")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
            
    else:
        form=AuthenticationForm()
    context={
        'form':form
    }
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')