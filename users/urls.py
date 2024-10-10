from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, PasswordResetView, UserProfileDetailView, UserProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_verification'),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    
    path('users/', UserProfileDetailView.as_view(), name='profile'),
    path('users/update/', UserProfileUpdateView.as_view(), name='profile_update'),
]
