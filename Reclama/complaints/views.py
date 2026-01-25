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
import complaints.forms as complaintsforms
import complaints.models as complaintsmodels
import defaults.models as defaultsmodels

#CONST_VARIABLES
dict_object_types = {'user':defaultsmodels.ObjectTypes.USER,'complaint':defaultsmodels.ObjectTypes.COMPLAINT}
dict_user_types = {'customer':defaultsmodels.UserTypes.CUSTOMER,'company':defaultsmodels.UserTypes.COMPANY}


@api_view(['POST','GET'])
def create_complaint_view(request,user_id,company_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    #must use deserialize to confirm if parameter type is correct

    parameter_user_account_id = user_id
    parameter_user_account_id_company = company_id

    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_user_account_id)

    object_user_account_company = accountsmodels.UserAccount.objects.filter(pk=parameter_user_account_id_company,user_type=dict_user_types['company'])

    if object_user_account and object_user_account_company:

        object_user_account_company = object_user_account_company[0]
        object_user_account = object_user_account[0]

        object_company = accountsmodels.Company.objects.get(user_account=object_user_account_company)


        if request.method == 'GET' or request.method == 'POST':

            if request.method == 'GET':

                #COMPANY INFO

                dict_company = {
                    "id":object_user_account_company.pk,
                    "name":object_company.name,
                    "logo":object_company.logo.url
                }

                dict_response['message'] = f"Create Complaint to {dict_company['name']} Company"
                dict_response['dict_company'] = dict_company


            else:

                request_data = request.data


                #DESERIALIZATION AND FORM VALIDATION

                deserializer_complaint = accountsserializers.CreateComplaintSerializer(data=request_data)

                if deserializer_complaint.is_valid():

                    deserialized_complaint = deserializer_complaint.validated_data
                    form_complaint = accountsforms.CreateComplaintForm(deserialized_complaint)

                    if form_complaint.is_valid():

                        cleaned_form_complaint = {
                            "title":form_complaint.cleaned_data.get('title'),
                            "body":form_complaint.cleaned_data.get('body')
                        }

                        instance_complaint = complaintsmodels.Complaint.objects.create(
                            author=object_user_account,
                            company=object_user_account_company,
                            title=cleaned_form_complaint['title'],
                            body=cleaned_form_complaint['body']
                        )

                        instance_complaint.save()

                        dict_response['message'] = "Complaint Created"


                    else:
                        dict_error['value'] = True
                        dict_error['status'] = status.HTTP_400_BAD_REQUEST
                        dict_error['description'] = "Invalid Complaint Submitted Data"

                else:

                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Complaint Request Data"


        #Invalid request
        else:
            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request"

    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['GET'])
def read_complaint_view(request,user_id,complaint_id):

    dict_response = {}
    sorted_list_dict_comment = []
    list_dict_comment = []

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_complaint_id = complaint_id
    parameter_user_account_id = user_id
    object_complaint = accountsmodels.Complaint.objects.filter(pk=parameter_complaint_id)
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)

    is_author = False
    is_company = False
    is_favourite = False

    if object_complaint and object_user_account:


        object_complaint = object_complaint[0]
        object_user_account = object_user_account[0]


        #Check if complaint is favourite

        object_favourite = accountsmodels.Favourite.objects.filter(user_account=object_user_account,foreign_int=object_complaint.pk,object_type=dict_object_types['complaint'])


        if object_favourite:

            is_favourite = True
        else:

            pass


        #COMPLAINT INFO

        dict_complaint = {
            "id":object_complaint.pk,
            "title":object_complaint.title,
            "body":object_complaint.body,
            "date_created":object_complaint.date_created,
            "is_active":object_complaint.is_active,
            "is_solved":object_complaint.is_solved,
            "is_favourite":is_favourite,
            "score_type":object_complaint.score_type
        }


        #AUTHOR INFO

        object_user_account_author = object_complaint.author


        if object_user_account_author.user_type == dict_user_types['customer']:

            object_profile_author = accountsmodels.Customer.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.full_name
            image_author = object_profile_author.profile_image.url

        else:

            object_profile_author = accountsmodels.Company.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.name
            image_author = object_profile_author.logo.url


        dict_author = {
            "id":object_user_account_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_user_account_company = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_user_account_company.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }


        #CHECK IF REQUESTING USER IS EITHER AUTHOR/COMPANY OF THE COMPLAINT

        if object_user_account == object_user_account_author or object_user_account == object_company_user_account:

            if object_user_account == object_user_account_author:

                is_author = True

            else:

                is_company = True

        #Just a regular user reading the complaint
        else:
            pass


        #COMMENTS

        list_object_comment = complaintsmodels.ComplaintComment.objects.filter(complaint=object_complaint)

        #check for comments
        if list_object_comment:

            for object_comment in list_object_comment:

                object_user_account_author_comment = object_comment.author

                #check if author is a customer
                if object_user_account_author_comment.user_type == dict_user_types['customer']:

                    object_profile_author_comment = accountsmodels.Customer.objects.get(user_account=object_user_account_author_comment)

                    name_author_comment = object_profile_author_comment.full_name
                    image_author_comment = object_profile_author_comment.profile_image.url

                else:

                    object_profile_author_comment = accountsmodels.Company.objects.get(user_account=object_user_account_author_comment)

                    name_author_comment = object_profile_author_comment.name
                    image_author_comment = object_profile_author_comment.logo.url


                dict_author_comment = {
                    "id":object_user_account_author_comment.pk,
                    "name":name_author_comment,
                    "image":image_author_comment
                }

                dict_comment = {
                    'id':object_comment.pk,
                    'body':object_comment.body,
                    'date_created':object_comment.date_created,
                    'dict_author':dict_author_comment
                }


                list_dict_comment.append(dict_comment)

            #To sort comments by date_created
            sorted_list_dict_comment = {sorted(list_dict_comment, key=lambda x: x['date_created'], reverse=False)}

        #No comments
        else:
            pass


        #COMPLAINT INFO

        dict_complaint = {
            "complaint":object_complaint.pk,
            "title":object_complaint.title,
            "body":object_complaint.body,
            "date_created":object_complaint.date_created,
            "is_active":object_complaint.is_active,
            "is_solved":object_complaint.is_solved,
            "is_favourite":is_favourite,
            "score_type":object_complaint.score_type
        }

        if request.method == "GET":

            dict_response['message'] = "Read Complaint"
            dict_response['dict_complaint'] = dict_complaint
            dict_response['dict_author'] = dict_author
            dict_response['dict_company'] = dict_company
            dict_response['list_dict_comment'] = sorted_list_dict_comment


        #Invalid request
        else:
            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request"

    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['POST','GET'])
def update_complaint_view(request,user_id,complaint_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }


    parameter_complaint_id = complaint_id
    parameter_user_account_id = user_id
    object_complaint = accountsmodels.Complaint.objects.filter(pk=parameter_complaint_id)
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_user_account:


        object_complaint = object_complaint[0]
        object_user_account = object_user_account[0]


        #COMPLAINT INFO

        dict_complaint = {
            "id":object_complaint.pk,
            "title":object_complaint.title,
            "body":object_complaint.body,
            "date_created":object_complaint.date_created,
            "is_active":object_complaint.is_active,
            "is_solved":object_complaint.is_solved,
            "score_type":object_complaint.score_type
        }


        #AUTHOR INFO

        object_user_account_author = object_complaint.author


        if object_user_account_author.user_type == dict_user_types['customer']:

            object_profile_author = accountsmodels.Customer.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.full_name
            image_author = object_profile_author.profile_image.url

        else:

            object_profile_author = accountsmodels.Company.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.name
            image_author = object_profile_author.logo.url


        dict_author = {
            "id":object_user_account_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_user_account_company = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_user_account_company.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }


        #check if both author and user are the same person
        if object_user_account == object_user_account_author:

            #check if complaint is open
            if dict_complaint['is_active'] == True:

                if request.method == 'GET' or request.method == 'POST':

                    if request.method == 'GET':

                        dict_response['message'] = "Update Complaint"
                        dict_response['complaint'] = {
                            'complaint':dict_complaint,
                            'author':dict_author,
                            'company':dict_company
                        }

                    else:

                        request_data = request.data


                        #DESERIALIZATION AND FORM VALIDATION

                        deserializer_complaint = accountsserializers.UpdateComplaintSerializer(data=request_data)

                        if deserializer_complaint.is_valid():

                            deserialized_complaint = deserializer_complaint.validated_data
                            form_complaint = accountsforms.UpdateComplaintForm(deserialized_complaint,instance=object_complaint)

                            if form_complaint.is_valid():

                                form_complaint.save()
                                dict_response['message'] = "Complaint Updated!"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Request Data"


                        else:

                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid Request Data"


                #INVALID REQUEST
                else:

                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Request"

            else:

                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Request Data"

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request Data"


    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['POST','GET'])
def close_complaint_view(request,user_id,complaint_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }


    parameter_complaint_id = complaint_id
    parameter_user_account_id = user_id
    object_complaint = accountsmodels.Complaint.objects.filter(pk=parameter_complaint_id)
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_user_account:


        object_complaint = object_complaint[0]
        object_user_account = object_user_account[0]


        #COMPLAINT INFO

        dict_complaint = {
            "id":object_complaint.pk,
            "title":object_complaint.title,
            "body":object_complaint.body,
            "date_created":object_complaint.date_created,
            "is_active":object_complaint.is_active,
            "is_solved":object_complaint.is_solved,
            "score_type":object_complaint.score_type
        }


        #AUTHOR INFO

        object_user_account_author = object_complaint.author


        if object_user_account_author.user_type == dict_user_types['customer']:

            object_profile_author = accountsmodels.Customer.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.full_name
            image_author = object_profile_author.profile_image.url

        else:

            object_profile_author = accountsmodels.Company.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.name
            image_author = object_profile_author.logo.url


        dict_author = {
            "id":object_user_account_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_user_account_company = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_user_account_company.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }

        #check if both author and user are the same person
        if object_user_account == object_user_account_author:

            #check if complaint is open
            if dict_complaint['is_active'] == True:

                if request.method == 'GET' or request.method == 'POST':

                    if request.method == 'GET':

                        dict_response['message'] = "Close Complaint"
                        dict_response['complaint'] = {
                            'complaint':dict_complaint,
                            'author':dict_author,
                            'company':dict_company
                        }


                    else:


                        request_data = request.data


                        #DESERIALIZATION AND FORM VALIDATION

                        deserializer_complaint = accountsserializers.CloseComplaintSerializer(data=request_data)

                        if deserializer_complaint.is_valid():

                            deserialized_complaint = deserializer_complaint.validated_data
                            form_complaint = accountsforms.CloseComplaintForm(deserialized_complaint,instance=object_complaint)

                            if form_complaint.is_valid():

                                #Save complaint instance by updating is_active field
                                instance_complaint = form_complaint.save(commit=False)
                                instance_complaint.is_active = False

                                form_complaint.save()
                                dict_response['message'] = "Complaint Closed!"

                            else:

                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Request Data"


                        else:

                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid Request Data"

                else:
                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Request"

            else:
                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Request Data"

        else:

            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request Data"


    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['GET'])
def list_complaint_user_view(request,user_id):

    dict_response = {}
    list_dict_complaint = []
    sorted_list_dict_complaint = []

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_user_account_id = user_id
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_user_account:

        object_user_account = object_user_account[0]
        list_object_complaint = complaintsmodels.Complaint.objects.filter(author=object_user_account)

        #check if user has created complaints
        if list_object_complaint:

            for object_complaint in list_object_complaint:

                dict_complaint = {
                    "id":object_complaint.pk,
                    "title":object_complaint.title,
                    "body":object_complaint.body,
                    "date_created":object_complaint.date_created,
                    "is_active":object_complaint.is_active,
                    "is_solved":object_complaint.is_solved,
                    "score_type":object_complaint.score_type
                }

                list_dict_complaint.append(dict_complaint)

            sorted_list_dict_complaint = sorted(list_dict_complaint, key=lambda x: x['title'], reverse=False)

        else:
            #no complaints
            pass

        if request.method == 'GET':

            dict_response['message'] = "User Complaints"
            dict_response['list_dict_complaint'] = sorted_list_dict_complaint

        else:
            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid Request"
    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"

    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])


@api_view(['GET'])
def list_complaint_view(request):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    list_dict_complaint = []
    sorted_list_dict_complaint = []

    list_object_complaint = complaintsmodels.Complaint.objects.all()


    #check if there are complaints
    if list_object_complaint:

        for object_complaint in list_object_complaint:

            dict_complaint = {
                "id":object_complaint.pk,
                "title":object_complaint.title,
                "body":object_complaint.body,
                "date_created":object_complaint.date_created,
                "is_active":object_complaint.is_active,
                "is_solved":object_complaint.is_solved,
                "score_type":object_complaint.score_type
            }

            list_dict_complaint.append(dict_complaint)


        sorted_list_dict_complaint = sorted(list_dict_complaint, key=lambda x: x['title'], reverse=False)

    else:

        #No complaints
        pass


    if request.method == 'GET':

        dict_response['message'] = "All Complaints"
        dict_response['sorted_list_dict_complaint'] = sorted_list_dict_complaint

    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request"
    
    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])



@api_view(['POST','GET'])
def create_comment_view(request,user_id,complaint_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    valid_user = False

    parameter_complaint_id = complaint_id
    parameter_user_account_id = user_id
    object_complaint = accountsmodels.Complaint.objects.filter(pk=parameter_complaint_id)
    object_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_user_account:


        object_complaint = object_complaint[0]
        object_user_account = object_user_account[0]


        #COMPLAINT INFO

        dict_complaint = {
            "id":object_complaint.pk,
            "title":object_complaint.title,
            "body":object_complaint.body,
            "date_created":object_complaint.date_created,
            "is_active":object_complaint.is_active,
            "is_solved":object_complaint.is_solved,
            "score_type":object_complaint.score_type
        }


        #AUTHOR INFO

        object_user_account_author = object_complaint.author


        if object_user_account_author.user_type == dict_user_types['customer']:

            object_profile_author = accountsmodels.Customer.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.full_name
            image_author = object_profile_author.profile_image.url

        else:

            object_profile_author = accountsmodels.Company.objects.get(user_account=object_user_account_author)
            name_author = object_profile_author.name
            image_author = object_profile_author.logo.url


        dict_author = {
            "id":object_user_account_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_user_account_company = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_user_account_company.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }


        #CHECK IF REQUESTING USER IS AUTHOR/COMPANY OF THE COMPLAINT

        if object_user_account == object_user_account_author or object_user_account == object_company_user_account:

            #check if complaint is open
            if dict_complaint['is_active'] == True:

                if request.method == 'GET' or request.method == 'POST':

                    if request.method == 'GET':

                        dict_response['message'] = "Create Comment"
                        dict_response['complaint'] = {
                            'complaint':dict_complaint,
                            'author':dict_author,
                            'company':dict_company
                        }

                    else:

                        request_data = request.data


                        #DESERIALIZATION AND FORM VALIDATION

                        deserializer_comment = complaintsserializers.CreateCommentSerializer(data=request_data)

                        if deserializer_comment.is_valid():

                            deserialized_comment = deserializer_comment.validated_data
                            form_comment = complaintsserializers.CreateCommentSerializer(deserialized_comment)

                            if form_comment.is_valid():

                                body_comment = form_comment.cleaned_data.get('body')

                                instance_comment = complaintsmodels.ComplaintComment.objects.create(
                                    author=object_user_account,
                                    complaint=object_complaint,
                                    body=body_comment
                                )

                                instance_comment.save()

                                dict_comment = {
                                    'body':body_comment
                                }

                                dict_response['message'] = "Comment Created!"
                                dict_response['dict_comment'] = dict_comment

                            else:
                                dict_error['value'] = True
                                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                                dict_error['description'] = "Invalid Request Parameters"


                        else:
                            dict_error['value'] = True
                            dict_error['status'] = status.HTTP_400_BAD_REQUEST
                            dict_error['description'] = "Invalid Request Parameters"


                else:
                    dict_error['value'] = True
                    dict_error['status'] = status.HTTP_400_BAD_REQUEST
                    dict_error['description'] = "Invalid Request"
            else:
                dict_error['value'] = True
                dict_error['status'] = status.HTTP_400_BAD_REQUEST
                dict_error['description'] = "Invalid Request Parameters"

        else:
            dict_error['value'] = True
            dict_error['status'] = status.HTTP_400_BAD_REQUEST
            dict_error['description'] = "Invalid User"

    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"
    
    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])
