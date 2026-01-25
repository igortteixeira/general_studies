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
import complaints.models as complaintsmodels
import defaults.models as defaultsmodels
import home.models as homemodels



#CONST_VARIABLES
dict_object_types = {'user':defaultsmodels.ObjectTypes.USER,'complaint':defaultsmodels.ObjectTypes.COMPLAINT}
dict_user_types = {'customer':defaultsmodels.UserTypes.CUSTOMER,'company':defaultsmodels.UserTypes.COMPANY}


@api_view(['GET'])
def list_search_view(request,search_string):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    list_dict_search_result = []
    sorted_list_dict_search_result = []

    #must use deserializer to confirm if parameter type is correct
    parameter_search_string = search_string

    #if user passed some arguments
    if parameter_search_string:

        list_object_user_account_company = accountsmodels.UserAccount.objects.filter(user_type=dict_user_types['company'],name__icontains=parameter_search_string)

        list_object_complaint = complaintsmodels.Complaint.objects.filter(title__icontains=parameter_search_string)

        #if there's company results
        if list_object_user_account_company:

            for object_user_account_company in list_object_user_account_company:

                object_company_profile = accountsmodels.Company.objects.filter(user_account=object_user_account_company)

                dict_company = {
                    'id':object_user_account_company.pk,
                    'name':object_company_profile.name,
                    'logo':object_profile.logo.url
                }

                list_dict_search_result.append(dict_company)

        #no complaint results
        else:
            pass

        #if there's complaint results
        if list_object_complaint:

            for object_complaint in list_object_complaint:

                dict_complaint = {
                    'id':object_complaint.pk,
                    'name':object_company_profile.name
                }

                list_dict_search_result.append(dict_complaint)

        #No complaint results
        else:
            pass

        sorted_list_dict_search_result = sorted(list_dict_search_result, key=lambda x: x['name'], reverse=False)


    #No arguments
    else:
        pass

        #GET Data

        if request.method == 'GET':

            dict_response['message'] = "Search List"
            dict_response['list_dict_search_result'] = sorted_list_dict_search_result

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request"


    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])
