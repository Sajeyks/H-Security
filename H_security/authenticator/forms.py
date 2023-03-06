from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext as _
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Profile, User
from django.contrib.auth import get_user_model



User = get_user_model()

# Forms go here

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
                                                                  'placeholder': 'Name',
                                                                  'class': 'form-control',
                                                                  }))
    
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
                                                                  'placeholder': 'Email',
                                                                  'class': 'form-control',}))
    
    phone_number = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='KE', attrs={
                                                                  'placeholder': 'Phone Number',
                                                                  'class': 'form-control',
                                                                  }))
    
    national_id_no = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
                                                                  'placeholder': 'Id/Birth Certificate No',
                                                                  'class': 'form-control',
                                                                  }))
    
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={
                                                                  'type': 'date',
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
        fields = ['name', 'email', 'phone_number', 'national_id_no', 'dob' , 'password1', 'password2']
        

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
        fields = ['name', 'password', 'remember_me']
        
        
class UpdateUserForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    phone_number = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='KE', attrs={
                                                                  'placeholder': 'Phone Number',
                                                                  'class': 'form-control',
                                                                  }))
    
    national_id_no = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
                                                                'placeholder': 'Id/Birth Certificate No',
                                                                'class': 'form-control',
                                                                }))
    
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={
                                                                  'type': 'date',
                                                                  'class': 'form-control',
                                                                  }))
    
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'national_id_no', 'dob']
        
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        

class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label=_("Email"), required=True)

    def confirm_login_allowed(self, user):
        UserModel = get_user_model()
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

        if self.cleaned_data.get('email') != user.email:
            raise forms.ValidationError(
                _("Please enter a correct email and password. Note that both fields may be case-sensitive."),
                code='invalid_login',
            )