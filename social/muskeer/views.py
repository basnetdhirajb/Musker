from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html',{})

@login_required(login_url='/')
def profiles(request):
    
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profiles.html',{'profiles':profiles})