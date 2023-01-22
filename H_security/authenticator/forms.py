from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext as _
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Profile, User

# User = get_user_model()

# Forms go here

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
                                                                  'placeholder': 'Username',
                                                                  'class': 'form-control',
                                                                  }))
    
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
                                                                  'placeholder': 'Email',
                                                                  'class': 'form-control',}))
    
    phone_number = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='KE', attrs={
                                                                  'placeholder': 'Phone Number',
                                                                  'class': 'form-control',
                                                                  }))
    
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={
                                                                  'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    
    password2 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={
                                                                  'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number' ,'password1', 'password2']
        

class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
        
        
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    phone_number = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='KE', attrs={
                                                                  'placeholder': 'Phone Number',
                                                                  'class': 'form-control',
                                                                  }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']
        
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']