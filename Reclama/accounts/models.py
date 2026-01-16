from django.db import models

import defaults.models as defaultsmodels


class UserAccount(models.Model):
    email = models.EmailField(max_length=60,unique=True)
    password = models.TextField()
    user_type = models.PositiveSmallIntegerField(choices=defaultsmodels.UserTypes.choices)



class Customer(models.Model):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=60,blank=True,default='Undefined')

    profile_image = models.ImageField(default='customer.png', upload_to='profile_pics')



#Add more fields such as overal quality and replies to customer complaints, view_count
class Company(models.Model):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    name = models.CharField(max_length=60,default='Undefined')
    description = models.TextField(blank=True,default='Undefined')
    location = models.CharField(max_length=60,blank=True,default='Undefined')
    phone_number = models.CharField(max_length=20,blank=True,default='Undefined')

    logo = models.ImageField(default='company.png', upload_to='profile_pics')


class Favorites(models.Model):
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)

    object_id = models.IntegerField()
    object_type = models.PositiveSmallIntegerField(choices=defaultsmodels.ObjectTypes.choices)