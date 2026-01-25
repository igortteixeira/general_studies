#Django Core
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

#REST FRAMEWORK
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser

#Personalized imports
import accounts.models as accountsmodels
import defaults.models as defaultsmodels
import accounts.forms as accountsforms
import accounts.serializers as accountsserializers


#CONST_VARIABLES
dict_object_types = {'user':defaultsmodels.ObjectTypes.USER,'complaint':defaultsmodels.ObjectTypes.COMPLAINT}
dict_user_types = {'customer':defaultsmodels.UserTypes.CUSTOMER,'company':defaultsmodels.UserTypes.COMPANY}



@api_view(['POST','GET'])
def create_user_view(request):

    dict_response = {}
    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    if request.method == 'GET' or request.method == 'POST':

        if request.method == 'GET':

            dict_response['message'] = "Create an Account"

        #POST REQUEST

        else:

            request_data = request.data

            #DESERIALIZATION AND FORM VALIDATION

            deserializer_user_account = accountsserializers.CreateUserAccountSerializer(data=request_data)

            if deserializer_user_account.is_valid():

                deserialized_user_account = deserializer_user_account.validated_data
                form_user_account = accountsforms.CreateUserAccountForm(deserialized_user_account)

                if form_user_account.is_valid():

                    cleaned_form_user_account = {
                        "email":form_user_account.cleaned_data.get('email'),
                        "password":form_user_account.cleaned_data.get('password'),
                        "password2":form_user_account.cleaned_data.get('password2'),
                        "user_type":form_user_account.cleaned_data.get('user_type')
                    }

                    #check if email is unique
                    valid_email = accountsforms.validate_cleaned_email(cleaned_form_user_account['email'])

                    #check if password is correct
                    valid_password = accountsforms.validate_cleaned_password(cleaned_form_user_account['password'],cleaned_form_user_account['password2'])

                    if valid_email and valid_password:

                        instance_user_account = accountsmodels.UserAccount.objects.create(
                            email=cleaned_form_user_account['email'],
                            password=cleaned_form_user_account['password2'],
                            user_type=cleaned_form_user_account['user_type']
                        )

                        if cleaned_form_user_account['user_type'] == dict_user_types['customer']:

                            deserializer_profile = accountsserializers.CreateCustomerSerializer(data=request_data)

                            if deserializer_profile.is_valid():

                                deserialized_profile = deserializer_profile.validated_data
                                form_profile = accountsforms.CreateCustomerForm(deserialized_profile)

                                if form_profile.is_valid():

                                    cleaned_form_profile = {
                                        "full_name":form_profile.cleaned_data.get('full_name')
                                    }

                                    #check for null values(to be improved)
                                    cleaned_form_profile = accountsforms.validate_null_fields(cleaned_form_user_account['user_type'],cleaned_form_profile)

                                else:

                                    dict_error['value'] = True
                                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                    dict_error['description'] = "Invalid Customer Submitted Data"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Customer Request Data"

                        else:

                            deserializer_profile = accountsserializers.CreateCompanySerializer(data=request_data)

                            if deserializer_profile.is_valid():

                                deserialized_profile = deserializer_profile.validated_data
                                form_profile = accountsforms.CreateCompanyForm(deserialized_profile)

                                if form_profile.is_valid():

                                    cleaned_form_profile = {
                                        "name":form_profile.cleaned_data.get('name'),
                                        "description":form_profile.cleaned_data.get('description'),
                                        "location":form_profile.cleaned_data.get('location'),
                                        "phone_number":form_profile.cleaned_data.get('phone_number')
                                    }

                                    #check for null values
                                    cleaned_form_profile = accountsforms.validate_null_fields(cleaned_form_user_account['user_type'],cleaned_form_profile)

                                else:

                                    dict_error['value'] = True
                                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                    dict_error['description'] = "Invalid Company Submitted Data"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Company Request Data"


                        instance_user_account.save()

                        if cleaned_form_user_account['user_type'] == dict_user_types['customer']:

                            instance_object = accountsmodels.Customer.objects.create(
                                user_account=instance_user_account,
                                full_name=cleaned_form_profile['full_name']
                            )

                        else:

                            instance_object = accountsmodels.Company.objects.create(
                                user_account=instance_user_account,
                                name=cleaned_form_profile['name'],
                                description=cleaned_form_profile['description'],
                                location=cleaned_form_profile['location'],
                                phone_number=cleaned_form_profile['phone_number']
                            )

                        instance_object.save()

                        dict_response['message'] = "Account Created"
                        dict_response['dict_user_account'] = cleaned_form_user_account
                        dict_response['dict_profile'] = cleaned_form_profile

                    else:
                        dict_error['value'] = True
                        dict_error['status'] = status.HTTP_400_BAD_REQUEST
                        dict_error['description'] = "Invalid Email Or Password"

                else:

                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid User Submitted Data"

            else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Request Data"

    #INVALID REQUEST
    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])



@api_view(['GET'])
def read_profile_user_view(request,user_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }


    #must use deserializer to confirm if parameter type is correct
    parameter_user_account_id = user_id

    if parameter_user_account_id:

        object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_user_account_id)

        if object_user_account:

            object_user_account = object_user_account[0]

            dict_user_account = {
                'id':object_user_account.pk,
                'email':object_user_account.email,
                'user_type':object_user_account.user_type
            }

            if dict_user_account['user_type'] == dict_user_types['customer']:

                object_profile = accountsmodels.Customer.objects.filter(user_account=object_user_account)
                object_profile = object_profile[0]

                dict_profile = {
                    'id':object_profile.pk,
                    'full_name':object_profile.full_name,
                    'profile_image':object_profile.profile_image.url
                }

            else:

                object_profile = accountsmodels.Company.objects.filter(user_account=object_user_account)
                object_profile = object_profile[0]

                dict_profile = {
                    'id':object_profile.pk,
                    'name':object_profile.name,
                    'description':object_profile.description,
                    'location':object_profile.location,
                    'phone_number':object_profile.phone_number,
                    'logo':object_profile.logo.url
                }

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request Data"

    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    if request.method == 'GET':

        dict_response['dict_user'] = {
            'account':dict_user_account,
            'profile':dict_profile
        }


    #Invalid request
    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['POST','GET'])
def create_favourite_view(request):

    dict_response = {}
    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    if request.method == 'GET' or request.method == 'POST':

        if request.method == 'GET':

            dict_response['message'] = "Create Favourite Object"

        else:
            
            request_data = request.data

            #DESERIALIZATION AND FORM VALIDATION

            deserializer_favourite = accountsserializers.CreateFavouriteSerializer(data=request_data)

            if deserializer_favourite.is_valid():

                deserialized_favourite = deserializer_favourite.validated_data
                form_favourite = accountsforms.CreateFavouriteForm(deserialized_favourite)

                if form_favourite.is_valid():

                    cleaned_form_favourite = {
                        "object_type":form_favourite.cleaned_data.get('object_type'),
                        "object_id":form_favourite.cleaned_data.get('object_id'),
                        "user_id":form_favourite.cleaned_data.get('user_id')
                    }

                    #check if it's a complaint post
                    if cleaned_form_favourite['object_type'] == dict_object_types['complaint']:

                        parameter_object = complaintsmodels.ComplaintPost.objects.filter(pk=cleaned_form_favourite['object_id'])

                    #check if it's company user
                    else:

                        parameter_object = accountsmodels.UserAccount.objects.filter(pk=cleaned_form_favourite['object_id'],user_type=dict_user_types['company'])

                    #check if parameter object is valid
                    if parameter_object:

                        parameter_object = parameter_object[0]

                        object_user_account = accountsmodels.UserAccount.objects.filter(pk=cleaned_form_favourite['user_id'])

                        if object_user_account:

                            object_user_account = object_user_account[0]

                            #Check if is not already user's favourite

                            object_favourite = homemodels.Favourite.objects.filter(pk=cleaned_form_favourite['object_id'],user_account=object_user_account)

                            if not object_favourite:

                                instance_favourite = homemodels.Favourite.objects.create(
                                    user_account=object_user_account,
                                    object_type=cleaned_form_favourite['object_type'],
                                    foreign_int=cleaned_form_favourite['object_id']
                                )

                                instance_favourite.save()

                                dict_response['message'] = "Added to Favourite"


                            else:

                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid Object Already Favourite"

                        else:

                        dict_error['value'] = True
                        dict_error['status'] = status.HTTP_400_BAD_REQUEST
                        dict_error['description'] = "Invalid Object User"


                    else:

                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Submitted Object"


                else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Favourite Submitted Data"


            else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Favourite Request Data"

    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])



@api_view(['POST','GET'])
def delete_favourite_view(request):

    dict_response = {}
    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    if request.method == 'GET' or request.method == 'POST':

        if request.method == 'GET':

            dict_response['message'] = "Delete Favourite Object"

        else:
            
            request_data = request.data

            #DESERIALIZATION AND FORM VALIDATION

            deserializer_favourite = accountsserializers.DeleteFavouriteSerializer(data=request_data)

            if deserializer_favourite.is_valid():

                deserialized_favourite = deserializer_favourite.validated_data
                form_favourite = accountsforms.DeleteFavouriteForm(deserialized_favourite)

                if form_favourite.is_valid():

                    cleaned_form_favourite = {
                        "favourite_id":form_favourite.cleaned_data.get('object_id'),
                        "user_account_id":form_favourite.cleaned_data.get('user_account_id')
                    }

                    object_user_account = accountsmodels.UserAccount.objects.filter(pk=cleaned_form_favourite['user_account_id'])

                    if object_user_account:

                        object_user_account = object_user_account[0]
                        object_favourite = accountsmodels.Favourite.objects.filter(pk=cleaned_form_favourite['favourite_id'])

                        #check if favourite exists
                        if object_favourite:

                            object_favourite = object_favourite[0]

                            #Check if both request user and favourite's user are the same person
                            if object_user_account == object_favourite.user_account:

                                object_favourite.delete()

                                dict_response['message'] = "Favourite Deleted!"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid User Id"

                        else:

                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid Favourite Id"

                    else:

                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Object Id"


                else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Favourite Submitted Data"


            else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Favourite Request Data"

    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


#Only Get in Debugging. Because the user must send it's credentials, but how? Post request? Must get from Authorization" header
@api_view(['GET'])
def list_favourite_user_view(request,user_id):

    dict_response = {}
    list_dict_favourite = []

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }


    parameter_user_account_id = user_id
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_user_account_id)

    if object_user_account:

        object_user_account = object_user_account[0]
        list_object_favourite = homemodels.Favourite.objects.filter(user_account=object_user_account)

        #check is results
        if list_object_favourite:

            for object_favourite in list_object_favourite:

                list_dict_favourite.append({'id':object_favourite.pk,'object_id':object_favourite.object_id,'object_type':object_favourite.object_type})

        else:
            pass


        if request.method == 'GET':

            dict_response['message'] = "User Favourite List"
            dict_response['list_dict_favourite'] = list_dict_favourite

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request"


    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid User Account Id"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])

