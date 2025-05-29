from django.urls import path
from users.views import (
    UserRegistrationView,
    UserLoginView,
    PasswordChangeView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationView,
    ForgotPasswordView,
    ResetPasswordConfirmView,
    GoogleLoginView,
)
from rest_framework_simplejwt.views import TokenRefreshView

# Authentication endpoints that will be prefixed with /api/
urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='api-register'),
    path('login', UserLoginView.as_view(), name='api-login'),
    path('verify-email', EmailVerificationView.as_view(), name='api-verify-email'),
    path('password/change', PasswordChangeView.as_view(), name='api-password-change'),
    path('password/reset', PasswordResetRequestView.as_view(), name='api-password-reset'),
    path('password/reset/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
    path('forgot-password', ForgotPasswordView.as_view(), name='api-forgot-password'),
    path('reset-password/confirm', ResetPasswordConfirmView.as_view(), name='api-reset-password-confirm'),
    path('auth/google', GoogleLoginView.as_view(), name='api-google-login'),
    
    # JWT Token endpoints
    path('token/refresh', TokenRefreshView.as_view(), name='api-token-refresh'),
]
