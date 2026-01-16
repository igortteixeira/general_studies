from rest_framework import serializers

import accounts.models as accountsmodels



class CreateUserAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    user_type = serializers.IntegerField()


class CreateCustomerSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, allow_blank=True)


class CreateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)



class CreateFavoriteSerializer(serializers.Serializer):
    object_type = serializers.IntegerField()
    object_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
