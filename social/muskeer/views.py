from django.shortcuts import render, redirect
from .models import Profile, Meep
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MeepForm, SignUpForm, UpdateUserForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
    userForm = SignUpForm()
    profileForm = ProfilePictureForm()
    if request.method == 'POST':
        userForm = SignUpForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password1']
            #firstName = form.cleaned_data['firstName']
            #lastName = form.cleaned_data['lastName']
            #email = form.cleaned_data['email']
            
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            
            #Set up profile picture
            userProfile = Profile.objects.get(user__id = user.id)
            profileForm = ProfilePictureForm(request.POST or None, request.FILES or None, instance= userProfile)
            
            if profileForm.is_valid():
                profileForm.save()
            else:
                messages.success(request, "Unable to upload profile picture!")
                
            messages.success(request, "You have been registered!")
            return redirect('home')
        else:
            messages.success(request, userForm.error_messages)
            
    return render(request, 'register.html', {'userForm': userForm, 'profileForm':profileForm})
    
def updateProfile(request):

    if request.user.is_authenticated:
        currentUser = User.objects.get(id = request.user.id)
        profileUser = Profile.objects.get(user__id = request.user.id)
        userForm = UpdateUserForm(request.POST or None, instance = currentUser)
        profileForm = ProfilePictureForm(request.POST or None, request.FILES or None, instance = profileUser)
        
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            login(request,currentUser)
            messages.success(request, ("Your profile has been updated"))
            return redirect('home')
        
        return render(request, 'update_profile.html', {'userForm':userForm, 'profileForm':profileForm})
    else:
        messages.success(request, 'You must be logged in to view this page!')
        return redirect('home')
    
def likeMeep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id = pk)
        if meep.likes.filter(id = request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        
        #print(request.META.get('HTTP_REFERER'))
        #Gives what page we are getting the request from to this view
        return redirect(request.META.get('HTTP_REFERER'))
            
    else:
        messages.success(request,("You must be logged in to view this page!"))
        return redirect('home')
    
def shareMeep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep:
            return render(request,'show_meep.html',{'meep':meep})
        else:
            messages.success(request, ('Meep does not exist!'))
            return redirect('home')

def unfollowUser(request, pk):
    if request.user.is_authenticated:
        #get the user to unfollow
        profileToUnfollow = Profile.objects.get(user_id = pk)
        #unfollow user
        request.user.profile.follows.remove(profileToUnfollow)
        #save profile
        request.user.profile.save()
        
        messages.success(request, (f"Unfollowed {profileToUnfollow.user.username}"))
        #Gives what page we are getting the request from to this view
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')

def followUser(request, pk):
        if request.user.is_authenticated:
            profileToFollow = Profile.objects.get(user_id = pk)
            request.user.profile.follows.add(profileToFollow)
            request.user.profile.save()
            
            messages.success(request, (f"Started Following {profileToFollow}"))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('home')
        
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            followers = request.user.profile.followed_by.all()
            return render(request, 'followers.html', {'followers': followers})
            
        else:
            messages.success(request, ("You caannot view this page!")) 
            return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def follows(request, pk):
    if request.user.is_authenticated:
        
        if request.user.id == pk:
            follows = request.user.profile.follows.all()
            return render(request, 'follows.html', {'follows': follows})
            
        else:
            messages.success(request, ("You caannot view this page!")) 
            return redirect('home')
        
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def deleteMeep(request, pk):
    if request.user.is_authenticated:
        meepToDelete = get_object_or_404(Meep, id = pk)
        if meepToDelete.user.id == request.user.id:
            #Able to delete the meep
            meepToDelete.delete()
            messages.success(request, ("Meep Deleted!"))
        else:
            messages.success(request, ("Not your Meep"))
        return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def editMeep(request, pk):
    if request.user.is_authenticated:
        meepToEdit = get_object_or_404(Meep, id = pk)
        form = MeepForm(request.POST or None, instance= meepToEdit)
        if meepToEdit.user.id == request.user.id:
            if request.method == 'POST':
                if form.is_valid():
                    meepToEdit = form.save(commit=False)
                    meepToEdit.save()
                    messages.success(request, ("Your meep has been updated!"))
                    return redirect('home')
            else:
                return render(request, 'edit_meep.html', {'form': form, 'meep': meepToEdit})
        else:
            messages.success(request, ("This is not your Meep to edit"))
            return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        messages.success(request, ("You have to log in to view this page"))
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        meepSearch = request.POST['search']
        meepResult = Meep.objects.filter(body__contains = meepSearch)
        
        userResult = User.objects.filter(username__contains = meepSearch)
        return render(request, 'search.html', {'meepResult':meepResult, 'meepSearch': meepSearch, 'userResult': userResult})
    else:
        return render(request, 'search.html', {})   