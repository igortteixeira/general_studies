from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class FriendRelation(models.Model):
    self_user = models.ForeignKey(User,on_delete=models.CASCADE)
    friend_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend_user_set')

    date_created = models.DateTimeField(default=timezone.now)


class FriendRequest(models.Model):
    requesting_user = models.ForeignKey(User,on_delete=models.CASCADE)
    requested_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='requested_user_set')

    date_created = models.DateTimeField(default=timezone.now)
