from rest_framework import serializers

import defaults.models as defaultsmodels
import accounts.models as accountsmodels



class CreateUserSerializer(serializers.ModelSerializer):
    password2 = models.TextField(null=False, blank=False)

    class Meta:
        model = accountsmodels.UserAccount
        fields = ['email', 'name', 'password', 'user_type']


class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountsmodels.CustomerProfile
        fields = ['user_Account','profile_image']


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = accountsmodels.CompanyProfile
        fields = ['email', 'name', 'password', 'user_type','profile_image']