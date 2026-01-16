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

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    #check request type and send appropriate response
    if request.method == 'GET' or request.method == 'POST':

        if request.method == 'GET':

            dict_response = {
                'message':"Create An Account"
            }

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

                            deserializer_object = accountsserializers.CreateCustomerSerializer(data=request_data)

                            if deserializer_object.is_valid():

                                deserialized_object = deserializer_object.validated_data
                                form_object = accountsforms.CreateCustomerForm(deserialized_object)

                                if form_object.is_valid():

                                    cleaned_form = {
                                        "full_name":form_object.cleaned_data.get('full_name')
                                    }

                                    #check for null values(to be improved)
                                    cleaned_form = accountsforms.validate_null_fields(cleaned_form_user_account['user_type'],cleaned_form)

                                else:

                                    dict_error['value'] = True
                                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                    dict_error['description'] = "Invalid Customer Submitted Data"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Customer Request Data"

                        else:

                            deserializer_object = accountsserializers.CreateCompanySerializer(data=request_data)

                            if deserializer_object.is_valid():

                                deserialized_object = deserializer_object.validated_data
                                form_object = accountsforms.CreateCompanyForm(company_deserialized)

                                if form_object.is_valid():

                                    cleaned_form = {
                                        "name":form_object.cleaned_data.get('name'),
                                        "description":form_object.cleaned_data.get('description'),
                                        "location":form_object.cleaned_data.get('location'),
                                        "phone_number":form_object.cleaned_data.get('phone_number')
                                    }

                                    #check for null values
                                    cleaned_form = accountsforms.validate_null_fields(cleaned_form_user_account['user_type'],cleaned_form)

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
                                full_name=cleaned_form['full_name']
                            )

                            object_instance.save()
                            dict_response['user_type_dict'] = customer_form_cleaned

                        else:

                            instance_object = accountsmodels.Company.objects.create(
                                user_account=instance_user_account,
                                name=cleaned_form['name'],
                                description=cleaned_form['description'],
                                location=cleaned_form['location'],
                                phone_number=cleaned_form['phone_number']
                            )

                        instance_object.save()

                        dict_response['dict_user'] = {
                            "dict_user_account":cleaned_form_user_account,
                            "dict_profile":cleaned_form
                        }

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
                dict_error['description'] = "Invalid User Request Data"

    #INVALID REQUEST
    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])



@api_view(['GET'])
def user_profile_view(request,id_parameter):

    dict_response = {}
    dict_user = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    if request.method == 'GET':

        user_id = id_parameter

        if user_id:

            user_account_object = accountsmodels.UserAccount.objects.filter(pk=user_id)

            if user_account_object:

                user_account_object = user_account_object[0]
                user_account_type = user_account_object.user_type

                if user_account_type == user_types_dict['customer']:

                    customer_object = accountsmodels.Customer.objects.filter(user_account=user_account_object)
                    customer_object = customer_object[0]

                    #To be improved

                    dict_user = {
                        'id':user_account_object.pk,
                        'email':user_account_object.email,
                        'profile_image':customer_object.profile_image.url,
                        'full_name':customer_object.full_name
                    }

                else:

                    company_object = accountsmodels.Company.objects.filter(user_account=user_account_object)
                    company_object = company_object[0]

                    dict_user = {
                        'id':user_account_object.pk,
                        'email':user_account_object.email,
                        'name':company_object.name,
                        'description':company_object.description,
                        'location':company_object.location,
                        'phone_number':company_object.phone_number,
                        'logo':company_object.logo.url
                    }


            else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Request Parameters"

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Missing Parameters"


    #Invalid request
    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_user']= dict_user
    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])




def favorite_view(request):

    context = {}

    request_user = c.user

    if request.method == 'POST':

        request_data = request.data

        #DESERIALIZATION AND FORM VALIDATION

        deserializer_favorite = accountsserializers.CreateFavoriteSerializer(data=request_data)

        if deserializer_favorite.is_valid():

            deserialized_favorite = deserializer_favorite.validated_data
            form_object = accountsforms.CreateFavoriteForm(deserialized_favorite)

            if form_object.is_valid():

                cleaned_form = {
                    "object_type":form_object.cleaned_data.get('object_type'),
                    "object_id":form_object.cleaned_data.get('object_id'),
                    "user_id":form_object.cleaned_data.get('user_id')
                }

                #check if it's a complaint post
                if cleaned_form['object_type'] == dict_object_types['complaint']:

                    object_to_favorite = complaintsmodels.ComplaintPost.objects.filter(pk=cleaned_form['object_id'])

                #check if it's company user
                else:

                    object_to_favorite = accountsmodels.UserAccount.objects.filter(pk=cleaned_form['object_id'],user_type=dict_user_types['company'])

                #check if parameter object is valid
                if object_to_favorite:

                    object_to_favorite = object_to_favorite[0]
                    object_favorite = homemodels.Favorites.objects.filter(pk=cleaned_form['object_id'])

                    #Check if is not already favorite
                    if not object_favorite:

                        object_user_account = accountsmodels.UserAccount.objects.filter(pk=cleaned_form['user_id'])

                        if object_user_account:

                            object_user_account = object_user_account[0]

                            instance_favorite = homemodels.Favorites.objects.create(
                                user_account=object_user_account,
                                object_type=cleaned_form['object_type'],
                                foreign_int=cleaned_form['object_id']
                            )

                            instance_favorite.save()


                            dict_response = {
                                'message':"Added to Favorite"
                            }

                        else:

                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid User Id"

                else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Object Id"


            else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Favorite Submitted Data"


        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Favorite Request Data"

    else:

        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])