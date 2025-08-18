from django.db import models
from django.contrib.auth.models import User



class FriendRelation(models.Model):
    first_user = models.ForeignKey(User,)
    second_user = models.ForeignKey(User,related_name='second_user_set')

    status = models.BooleanField()

    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField()