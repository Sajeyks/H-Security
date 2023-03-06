from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .forms import RegisterForm, LoginForm, UpdateProfileForm, UpdateUserForm, ResendActivationEmailForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model
from H_security.utils import Mail
from django.http import HttpResponse
from p_records.models import HealthRecord
# Create your views here.

User = get_user_model()


@login_required
def home(request):
    me = request.user
    my_record = HealthRecord.objects.get(owner=me)
    
    context = {
        "Recorddetails": my_record,
    }
    
    return render(request, "p_records/record-details.html", context)


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
            messages.success(request, f'Account created for {name}, check in your email for an account activation link')
            
            user_email = form.cleaned_data.get('email')
            user = User.objects.get(email=user_email)

            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-email')

            absurl = 'http://' + current_site + relativeLink + "?token=" + str(user.id)
            email_body = "Hi " + user.name + '! \nUse the link below to verify your email \n\n' + absurl
            data = {'email_body': email_body,'to_email': user.email,
                'email_subject':'Verify your email'}
            Mail.send_email(data)
        
            return redirect(to="/")
        return render(request, self.template_name, {'form': form})
    
    
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
            
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
    def form_invalid(self, form):
        # Check if the user is inactive
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(self.request, "Your account is not active. Please verify your email.")
        except User.DoesNotExist:
            pass
        return super(CustomLoginView, self).form_invalid(form)
    
    def get_success_url(self):
        if not self.request.user.is_active:
            # return reverse_lazy('inactive-account') resend-activation-email
            return reverse_lazy('resend-activation-email')
        else:
            return reverse_lazy('h-records')
    
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
    
    
def verifyEmailView(request):
    token = request.GET.get('token')
    try:
        user = User.objects.get(id=token)
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.save()
        return HttpResponse({'Succesfully verified and account activated'})

    except Exception as E:
        return HttpResponse(E)
    
    
def resendVerificationEmail(request):
    if request.method == 'POST':
        re_form = ResendActivationEmailForm(request.POST)
        
        if re_form.is_valid():
            user_email = re_form.cleaned_data.get('email')
            try:
                if  User.objects.filter(email=user_email).exists:
                    user = User.objects.get(email__exact=user_email)
                    current_site = get_current_site(request).domain
                    relativeLink = reverse('verify-email')

                    absurl = 'http://' + current_site + relativeLink + "?token=" + str(user.id)
                    email_body = "Hi " + user.name+ '! \nUse the link below to verify your email \n\n' + absurl
                    data = {'email_body': email_body,'to_email': user.email,
                        'email_subject':'Verify your email'}
                    Mail.send_email(data)
                    return HttpResponse({'Verification Email sent. Check your inbox.'})
                
            except User.DoesNotExist as exc:
                return HttpResponse({'The email address does not not match any user accont'})
        
            return HttpResponse("The actication email has been resend successfully.. check your inbox")
        
    else:
        re_form = ResendActivationEmailForm()
    context = {
        'form': re_form, 
        }
    
    return render(request, 'authenticator/resend_activation_email.html', context)
    