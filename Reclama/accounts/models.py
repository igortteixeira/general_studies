from django.contrib.auth.models import AbstractUser
from django.db import models

import defaults.models as defaultsmodels
from PIL import Image


class CustomUser(AbstractUser):

    user_type = models.PositiveSmallIntegerField(default=defaultsmodels.UserTypes.CUSTOMER,choices=defaultsmodels.UserTypes.choices)



class CustomerProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    name = models.CharField(max_length=60,blank=True,default='Undefined Name')

    profile_image = models.ImageField(default='customer.png', upload_to='profile_pics')

    def save(self,*args, **kwargs):
        super(CustomerProfile,self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)



#Add more fields such as overal quality and replies to customer complaints, view_count
class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    name = models.CharField(max_length=60,blank=True,default='Undefined Name')
    description = models.TextField(blank=True,default='Undefined Description')
    location = models.CharField(max_length=60,blank=True,default='Undefined Location')
    phone_number = models.CharField(max_length=40,blank=True,default='Undefined Phone Number')

    profile_image = models.ImageField(default='company.png', upload_to='profile_pics')

    def save(self,*args, **kwargs):
        super(CompanyProfile,self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
