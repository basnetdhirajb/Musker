from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profiles/', views.profiles, name = 'profiles'),
    path('profile/<int:pk>', views.profile, name = 'profile'),
    path('profile/followers/<int:pk>', views.followers, name = 'followers'),
    path('profile/follows/<int:pk>', views.follows, name = 'follows'),
    path('login/',  views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('update_profile/', views.updateProfile, name = 'update_profile'),
    path('meep_like/<int:pk>', views.likeMeep, name = 'likeMeep'),
    path('meep_share/<int:pk>', views.shareMeep, name = 'shareMeep'),
    path('meep_delete/<int:pk>', views.deleteMeep, name = 'deleteMeep'),
    path('unfollow/<int:pk>', views.unfollowUser, name = 'unfollowUser'),
    path('followUser/<int:pk>', views.followUser, name= 'followUser'),
]
