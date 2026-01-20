from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

import accounts.models as accountsmodels
import complaints.forms as complaintsforms
import complaints.models as complaintsmodels
import defaults.models as defaultsmodels
import home.models as homemodels

#CONST_VARIABLES
dict_object_types = {'user':defaultsmodels.ObjectTypes.USER,'complaint':defaultsmodels.ObjectTypes.COMPLAINT}
dict_user_types = {'customer':defaultsmodels.UserTypes.CUSTOMER,'company':defaultsmodels.UserTypes.COMPANY}


def create_complaint_view(request,company_id,requesting_user_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    #must use deserialize to confirm if parameter type is correct

    parameter_company_id = company_id
    parameter_requesting_user_id = requesting_user_id
    object_company_user = accountsmodels.UserAccount.objects.filter(pk=parameter_company_id,user_type=dict_user_types['company'])
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)

    if object_company_user and object_requesting_user_account:

        object_company_user = object_company_user[0]
        object_requesting_user_account = object_requesting_user_account[0]
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user)


        if object_requesting_user_account.user_type == dict_user_types['customer']:

            object_requesting_user_profile = accountsmodels.Customer.objects.get(user_account=object_requesting_user_account)
            object_requesting_user_profile_name = object_requesting_user_profile.full_name

        else:

            object_requesting_user_profile = accountsmodels.Company.objects.get(user_account=object_requesting_user_account)
            object_requesting_user_profile_name = object_requesting_user_profile.name



        if request.method == 'GET':

            #COMPANY INFO

            dict_company = {
                "id":object_requesting_user_account.pk,
                "name":object_company.name,
                "logo":object_company.logo.url
            }

            dict_response['message'] = "Create Complaint Post"
            dict_response['dict_company'] = dict_company


        elif request.method == 'POST':

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

                    instance_complaint = complaintsmodels.ComplaintPost.objects.create(
                        author=object_requesting_user_account,
                        company=object_company_user,
                        title=cleaned_form_complaint['title'],
                        body=cleaned_form_complaint['body']
                    )

                    instance_complaint.save()
                    
                    dict_response['dict_complaint'] = {
                        "author":object_requesting_user_profile_name,
                        "company":object_company.name,
                        "title":cleaned_form_complaint['title'],
                        "body":cleaned_form_complaint['body']
                    }


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


def read_complaint_view(request,complaint_id,requesting_user_id):

    dict_response = {}
    list_comments = []

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_complaint_id = complaint_id
    parameter_requesting_user_id = requesting_user_id
    object_complaint = accountsmodels.ComplaintPost.objects.filter(pk=parameter_complaint_id)
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)

    is_author = False
    is_company = False
    are_comments = False
    is_favorite = False
    favorite_id = False

    if object_complaint and object_requesting_user_account:


        object_complaint = object_complaint[0]
        object_requesting_user_account = object_requesting_user_account[0]

        if request.method == 'GET':

            #Check if complaint is favorite

            object_favorite_complaint = accountsmodels.Favorites.objects.filter(user=object_requesting_user_account,foreign_int=object_complaint.pk,object_type=dict_object_types['complaint'])


            if object_favorite_complaint:

                is_favorite = True
                object_favorite_complaint = object_favorite_complaint[0]

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
                "is_favorite":is_favorite,
                "score_type":object_complaint.score_type
            }


            #AUTHOR INFO

            object_author_user_account = object_complaint.author


            if object_author_user_account.user_type == dict_user_types['customer']:

                object_author_profile = accountsmodels.Customer.objects.get(user_account=object_author_user_account)
                name_author = object_author_profile.full_name
                image_author = object_author_profile.profile_image.url

            else:

                object_author_profile = accountsmodels.Company.objects.get(user_account=object_author_user_account)
                name_author = object_author_profile.name
                image_author = object_author_profile.logo.url


            dict_author = {
                "id":object_author.pk,
                "name":name_author,
                "image":image_author
            }


            #COMPANY INFO

            object_company_user_account = object_complaint.company
            object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

            dict_company = {
                "id":object_company_user_account.pk,
                "name":object_company.name,
                "logo":object_company.logo.url
            }


            #CHECK IF REQUESTING USER IS EITHER AUTHOR/COMPANY OF THE COMPLAINT

            if object_requesting_user_account == object_author_user_account:

                is_author = True

            else:

                if object_requesting_user_account == object_company_user_account:

                    is_company = True

                #Just a regular user reading the complaint
                else:
                    pass


            #COMMENTS

            objects_comment = complaintsmodels.ComplaintComment.objects.filter(complaint_post=object_complaint)

            #check for comments
            if objects_comment:

                are_comments = True

                for object_comment in objects_comment:

                    object_author_user_account_comment = object_comment.author

                    #check if author is a customer
                    if object_author_user_account_comment.user_type == dict_user_types['customer']:

                        object_profile_author_comment = accountsmodels.Customer.objects.get(user_account=object_author_user_account_comment)

                        name_author_comment = object_profile_author_comment.full_name
                        image_author_comment = object_profile_author_comment.profile_image.url


                    else:

                        object_profile_author_comment = accountsmodels.Company.objects.get(user_account=object_profile_author_comment)

                        name_author_comment = object_profile_author_comment.name
                        image_author_comment = object_profile_author_comment.logo.url

                    dict_author_comment = {
                        "id":object_author_user_account_comment.pk,
                        "name":name_author_comment,
                        "image":image_author_comment
                    }


                    list_comments.append({
                        'id':object_comment.pk,
                        'body':object_comment.body,
                        'date_created':object_comment.date_created,
                        'author':dict_author
                    })

                #To sort comments by date_created
                dicts_comment = {sorted(list_comments, key=lambda x: x['date_created'], reverse=False)}

            #No comments
            else:
                pass

            dict_response['message'] = "Read Complaint Post"
            dict_response['dict_complaint'] = dict_complaint
            dict_response['dict_author'] = dict_author
            dict_response['dict_company'] = dict_company
            dict_response['dicts_comment'] = dicts_comment


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


def update_complaint_view(request,complaint_id,requesting_user_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_complaint_id = complaint_id
    parameter_requesting_user_id = requesting_user_id

    object_complaint = accountsmodels.ComplaintPost.objects.filter(pk=parameter_complaint_id)
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_requesting_user_account:

        object_complaint = object_complaint[0]
        object_requesting_user_account = object_requesting_user_account[0]


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

        object_author_user_account = object_complaint.author


        if object_author_user_account.user_type == dict_user_types['customer']:

            object_author_profile = accountsmodels.Customer.objects.get(user_account=object_author_user_account)
            name_author = object_author_profile.full_name
            image_author = object_author_profile.profile_image.url

        else:

            object_author_profile = accountsmodels.Company.objects.get(user_account=object_author_user_account)
            name_author = object_author_profile.name
            image_author = object_author_profile.logo.url


        dict_author = {
            "id":object_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_company_user_account = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_company_user_account.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }


        #check if both author and request users are the same person
        if object_requesting_user_account == object_author_user_account:


            #check if complaint is open
            if dict_complaint['is_active'] == True:

                if request.method == 'GET':

                    dict_response['message'] = "Update Complaint Post"
                    dict_response['dict_complaint'] = dict_complaint
                    dict_response['dict_author'] = dict_author
                    dict_response['dict_company'] = dict_company

                elif request.method == 'POST':

                    request_data = request.data


                    #DESERIALIZATION AND FORM VALIDATION

                    deserializer_complaint = accountsserializers.UpdateComplaintSerializer(data=request_data)

                    if deserializer_complaint.is_valid():

                        deserialized_complaint = deserializer_complaint.validated_data
                        form_complaint = accountsforms.UpdateComplaintForm(deserialized_complaint,instance=object_complaint)

                        if form_complaint.is_valid():

                            form_complaint.save()
                            dict_response['message'] = "Complaint Post Updated!"

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


def close_complaint_view(request,complaint_id,requesting_user_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_complaint_id = complaint_id
    parameter_requesting_user_id = requesting_user_id

    object_complaint = accountsmodels.ComplaintPost.objects.filter(pk=parameter_complaint_id)
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_requesting_user_account:

        object_complaint = object_complaint[0]
        object_requesting_user_account = object_requesting_user_account[0]


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

        object_author_user_account = object_complaint.author


        if object_author_user_account.user_type == dict_user_types['customer']:

            object_author_profile = accountsmodels.Customer.objects.get(user_account=object_author_user_account)
            name_author = object_author_profile.full_name
            image_author = object_author_profile.profile_image.url

        else:

            object_author_profile = accountsmodels.Company.objects.get(user_account=object_author_user_account)
            name_author = object_author_profile.name
            image_author = object_author_profile.logo.url


        dict_author = {
            "id":object_author.pk,
            "name":name_author,
            "image":image_author
        }


        #COMPANY INFO

        object_company_user_account = object_complaint.company
        object_company = accountsmodels.Company.objects.get(user_account=object_company_user_account)

        dict_company = {
            "id":object_company_user_account.pk,
            "name":object_company.name,
            "logo":object_company.logo.url
        }


        #check if both author and request users are the same person
        if object_requesting_user_account == object_author_user_account:

            if dict_complaint['is_active'] == True:
            

                if request.method == 'GET':

                    dict_response['message'] = "Close Complaint Post"
                    dict_response['dict_complaint'] = dict_complaint
                    dict_response['dict_author'] = dict_author
                    dict_response['dict_company'] = dict_company
                    dict_response['dict_comments'] = dict_comments


                elif request.method == 'POST':


                    request_data = request.data


                    #DESERIALIZATION AND FORM VALIDATION

                    deserializer_complaint = accountsserializers.UpdateComplaintSerializer(data=request_data)

                    if deserializer_complaint.is_valid():

                        deserialized_complaint = deserializer_complaint.validated_data
                        form_complaint = accountsforms.UpdateComplaintForm(deserialized_complaint,instance=object_complaint)

                        if form_complaint.is_valid():

                            #Save complaint instance by updating is_ative field
                            instance_complaint = form_complaint.save(commit=False)
                            instance_complaint.is_active = False

                            form_complaint.save()
                            dict_response['message'] = "Complaint Post Closed!"

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


def user_complaint_list_view(request,requesting_user_id):

    dict_response = {}
    sorted_dicts_complaint = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_requesting_user_id = requesting_user_id
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_requesting_user_account:

        object_requesting_user_account = object_requesting_user_account[0]

        if request.method == 'GET':

                objects_complaint = complaintsmodels.ComplaintPost.objects.filter(author=object_requesting_user_account)

                #check if user has created complaints
                if objects_complaint:

                    for object_complaint in objects_complaint:

                        dict_complaint = {
                            "id":object_complaint.pk,
                            "title":object_complaint.title,
                            "body":object_complaint.body,
                            "date_created":object_complaint.date_created,
                            "is_active":object_complaint.is_active,
                            "is_solved":object_complaint.is_solved,
                            "score_type":object_complaint.score_type
                        }

                        dicts_complaint.append(dict_complaint)

                    sorted_dicts_complaint = sorted(dicts_complaint, key=lambda x: x['title'], reverse=False)

                else:
                    #no complaints
                    pass

                dict_response['message'] = "User Complaint Posts"
                dict_response['dicts_complaint'] = sorted_dicts_complaint

        
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


def create_comment_view(request,complaint_id,requesting_user_id):

    dict_response = {}

    dict_error = {
        'value':False,
        'status':status.HTTP_200_OK,
        'description':"No error"
    }

    parameter_complaint_id = complaint_id
    parameter_requesting_user_id = requesting_user_id

    object_complaint = accountsmodels.ComplaintPost.objects.filter(pk=parameter_complaint_id)
    object_requesting_user_account = accountsmodels.UserAccount.objects.filter(pk=parameter_requesting_user_id)


    if object_complaint and object_requesting_user_account:

        object_complaint = object_complaint[0]
        object_requesting_user_account = object_requesting_user_account[0]


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


        object_author_user_account = object_complaint.author
        object_company_user_account = object_complaint.company


        #check if requesting user is either complaint author or comapny
        if object_requesting_user_account == object_author_user_account or object_requesting_user_account == object_company_user_account:


            #check if complaint is open
            if dict_complaint['is_active'] == True:

                if request.method == 'POST':


                    request_data = request.data


                    #DESERIALIZATION AND FORM VALIDATION

                    deserializer_comment = complaintsserializers.CreateCommentSerializer(data=request_data)

                    if deserializer_comment.is_valid():

                        deserialized_comment = deserializer_comment.validated_data
                        form_comment = complaintsserializers.CreateCommentSerializer(deserialized_comment)

                        if form_comment.is_valid():

                            body_comment = form_comment.cleaned_data.get('body')

                            instance_comment = complaintsmodels.ComplaintComment.objects.create(
                                author=object_requesting_user_account,
                                complaint_post=dict_complaint['id'],
                                body=body_comment
                            )

                            instance_comment.save()

                            dict_response['message'] = "Comment Created!"

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
            dict_error['description'] = "Invalid Request Parameters"

    else:
        dict_error['value'] = True
        dict_error['status'] = status.HTTP_400_BAD_REQUEST
        dict_error['description'] = "Invalid Request Parameters"
    
    dict_response['dict_error'] = dict_error
    return Response(dict_response,status=dict_error['status'])

def complaints_list_view(request):

    context = {}
    complaint_dicts_list = []
    sorted_complaint_dicts = []

    is_complaint = bool_states_no

    if request.method == 'GET':

        complaint_objects = complaintsmodels.ComplaintPost.objects.all()

        #check if there are complaints
        if complaint_objects:

            is_complaint = bool_states_yes

            for complaint_object in complaint_objects:

                complaint_id = complaint_object.pk
                complaint_title = complaint_object.title

                complaint_dicts_list.append({'id':complaint_id,'title':complaint_title})

            sorted_complaint_dicts = sorted(complaint_dicts_list, key=lambda x: x['title'], reverse=False)

        else:

            #No complaints
            pass


        #GET_DATA

        complaint_dicts = {'is_complaint':is_complaint,'dicts':sorted_complaint_dicts}

        defaults_dict = {'bool_states_dict':bool_states_dict}



        context['GET_data'] ={
            'complaint_dicts':complaint_dicts,
            'defaults_dict':defaults_dict
        }


        return render(request, "complaints/complaints_list.html",context)
    else:
        return HttpResponse("INVALID REQUEST!")
