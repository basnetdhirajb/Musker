from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

#unregister groups
admin.site.unregister(Group)
admin.site.unregister(User)

#Mix profile info into User
class ProfileInline(admin.StackedInline):
    model = Profile

#extend user class
class UserAdmin(admin.ModelAdmin):
    model = User
    #Just display username field on admin page
    fields = ["username"]
    inlines = [ProfileInline]



# Register your models here.
admin.site.register(User, UserAdmin)