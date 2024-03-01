from typing import Any
from django import forms
from .models import Meep, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True,
        widget = forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter your Meep here!",
                    "class" : "form-control",
                    }
            ),
        label="",
        )
    
    class Meta:
        model = Meep
        exclude = ["user", "likes"]
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget= forms.TextInput(attrs={
        "placeholder": "Email",
        "class" : "form-control"
    }))
    first_name = forms.CharField( max_length= 100 ,label="", widget= forms.TextInput(attrs={
        "placeholder": "First Name",
        "class" : "form-control"
    }))
    last_name = forms.CharField( max_length= 100 ,label="", widget= forms.TextInput(attrs={
        "placeholder": "Last Name",
        "class" : "form-control"
    }))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        #This is customized here because they cannot be done like we did for email, first name and last name
        #Overriding the default attributes and help texts
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class = "form-text text-muted"><small> Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. </small></span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class = "form-text text-muted"> <li><small>Your password can’t be too similar to your other personal information.</small></li> <li><small>Your password must contain at least 8 characters.</small></li> <li><small>Your password can’t be a commonly used password.</small></li> <li><small>Your password can’t be entirely numeric.</small></li> </ul>'
        
       
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class = "form-text text-muted small "><small> Enter the same password as before, for verification. </small></span>'
        
class UpdateUserForm(forms.ModelForm):
    
    email = forms.EmailField(label="", widget= forms.TextInput(attrs={
        "placeholder": "Email",
        "class" : "form-control"
    }))
    
    first_name = forms.CharField( max_length= 100 ,label="", widget= forms.TextInput(attrs={
        "placeholder": "First Name",
        "class" : "form-control"
    }))
    
    last_name = forms.CharField( max_length= 100 ,label="", widget= forms.TextInput(attrs={
        "placeholder": "Last Name",
        "class" : "form-control"
    }))
    
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        #This is customized here because they cannot be done like we did for first name and last name
        #Overriding the default attributes and help texts
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class = "form-text text-muted"><small> Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. </small></span>'
        
class ProfilePictureForm(forms.ModelForm):
    
    profileImage = forms.ImageField(label="Profile Picture")
    
    class Meta:
        model = Profile
        fields = ['profileImage']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['profileImage'].required = False
        