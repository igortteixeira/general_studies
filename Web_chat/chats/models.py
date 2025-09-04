from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class FriendsChat(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_user_set')

    body = models.TextField()

    date_created = models.DateTimeField(default=timezone.now)
