from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profiles/', views.profiles, name = 'profiles'),
    path('profile/<int:pk>', views.profile, name = 'profile'),
    path('login/',  views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('update_profile/', views.updateProfile, name = 'update_profile')
]
