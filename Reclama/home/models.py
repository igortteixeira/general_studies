from django.db import models

import accounts.models as accountsmodels
import defaults.models as defaultsmodels


class Favorites(models.Model):
    user = models.ForeignKey(accountsmodels.CustomUser,on_delete=models.CASCADE)

    name = models.CharField(max_length=60,default='Undefined')
    title = models.TextField(default='Undefined')
    foreign_int = models.IntegerField()
    object_type = models.PositiveSmallIntegerField(choices=defaultsmodels.ObjectTypes.choices)

    company_profile_image_url = models.CharField(max_length=20,default='Undefined')
