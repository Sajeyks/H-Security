from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateProfileForm, UpdateUserForm
# Create your views here.

def home(request):
    return render(request, 'authenticator/homepage.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'authenticator/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='login')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            form.save()
            
            name = form.cleaned_data.get('name')
            messages.success(request, f'Account created for {name}')
            
            return redirect(to="/")
        
        return render(request, self.template_name, {'form': form})
    
    
class CustomLoginView(LoginView):
    form_class = LoginForm
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
            
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authenticator/password_reset.html'
    email_template_name = 'authenticator/password_reset_email.html'
    subject_template_name = 'authenticator/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('homepage')
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
            
    context = {
        'user_form': user_form, 
        'profile_form': profile_form
        }
    
    return render(request, 'authenticator/profile.html', context)
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'authenticator/change_password.html'
    success_message = 'Successfully Changed Your Password'
    success_url = reverse_lazy('homepage')