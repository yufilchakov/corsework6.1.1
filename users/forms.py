from django.contrib.auth.forms import UserCreationForm
from mailing.forms import StyleFormMixin
from users.models import User
from django.forms import ModelForm


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс форма для пользователя"""
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        
        
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone_number', 'token']
