from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class FriendRelation(models.Model):
    first_user = models.ForeignKey(User,on_delete=models.CASCADE)
    second_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='second_user_set')

    status = models.BooleanField()

    date_created = models.DateTimeField(default=timezone.now)