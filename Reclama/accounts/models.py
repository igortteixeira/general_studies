from django.db import models

import defaults.models as defaultsmodels


class User(models.Model):
    email = models.EmailField(max_length=60,unique=True)
    password = models.TextField()
    user_type = models.PositiveSmallIntegerField(choices=defaultsmodels.UserTypes.choices)



class Customer(models.Model):
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=60,default='Undefined Full Name')

    profile_image = models.ImageField(default='customer.png', upload_to='profile_pics')



#Add more fields such as overal quality and replies to customer complaints, view_count
class Company(models.Model):
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=60)
    description = models.TextField()
    location = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=20)

    logo = models.ImageField(default='company.png', upload_to='profile_pics')


class Favorites(models.Model):
    user = models.ForeignKey(accountsmodels.CustomUser,on_delete=models.CASCADE)

    foreign_int = models.IntegerField()
    object_type = models.PositiveSmallIntegerField(choices=defaultsmodels.ObjectTypes.choices)