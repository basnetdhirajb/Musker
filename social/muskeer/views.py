from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html',{})

#@login_required(login_url='/')
def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, 'profiles.html',{'profiles':profiles})
    else:
        messages.success(request,("You must be logged in to view this page"))
        return redirect('home')
        
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = pk)
        
        #POST form logic
        if request.method == 'POST':
            #Get current user profile
            currentProfile = request.user.profile
            action = request.POST['follow']
            
            #Decide to follow or unfollow
            if action == "unfollow":
                currentProfile.follows.remove(profile)
            else:
                currentProfile.follows.add(profile)
            
            #save the profile
            currentProfile.save()
        
        return render(request, 'profile.html', {'profile': profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
    