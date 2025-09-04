from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Profile



class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]

'''
class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
'''


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']