from django import forms
from .models import FriendsChat



class FriendsChatForm(forms.ModelForm):
    class Meta:
        model = FriendsChat
        fields = ['body']