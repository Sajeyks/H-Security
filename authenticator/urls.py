from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, RegisterView, CustomLoginView, ResetPasswordView, profile, ChangePasswordView, resendVerificationEmail, verifyEmailView
from .forms import LoginForm

urlpatterns = [
    path('', home, name='homepage'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='authenticator/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authenticator/logout.html'), name='logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='authenticator/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='authenticator/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('verify-email/', verifyEmailView, name='verify-email'),
    path('resend-activation-email/', resendVerificationEmail, name='resend-activation-email'),
    
]