from django.shortcuts import render, redirect
from .models import Profile, Meep
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MeepForm, SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request,("Your meep has been posted"))
                return redirect('home')
        
        meeps = Meep.objects.all().order_by("-createdAt")
        return render(request, 'home.html',{'meeps':meeps, 'form': form})
    else:
        meeps = Meep.objects.all().order_by("-createdAt")
        return render(request, 'home.html',{'meeps':meeps})

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
        meeps = Meep.objects.filter(user = pk).order_by("-createdAt")
        
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
            
        
        return render(request, 'profile.html', {'profile': profile, 'meeps':meeps})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("Incorrect Credentials!"))
            return redirect('login')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def registerUser(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #firstName = form.cleaned_data['firstName']
            #lastName = form.cleaned_data['lastName']
            #email = form.cleaned_data['email']
            
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered!")
            return redirect('home')
        else:
            messages.success(request, form.error_messages)
    else:
        return render(request, 'register.html', {'form': form})
    
def updateProfile(request):

    if request.user.is_authenticated:
        currentUser = User.objects.get(id = request.user.id)
        form = UpdateUserForm(request.POST or None, instance = currentUser)
        
        if form.is_valid():
            form.save()
            login(request,currentUser)
            messages.success(request, ("Your profile has been updated"))
            return redirect('home')
        
        return render(request, 'update_profile.html', {'form':form})
    else:
        messages.success(request, 'You must be logged in to view this page!')
        return redirect('home')