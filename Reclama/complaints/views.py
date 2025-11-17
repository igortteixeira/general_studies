from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

import accounts.models as accountsmodels
import complaints.forms as complaintsforms
import complaints.models as complaintsmodels
import defaults.models as defaultsmodels

#ENV_VARIABLES
user_types_company = defaultsmodels.UserTypes.COMPANY
user_types_customer = defaultsmodels.UserTypes.CUSTOMER
bool_states_yes = defaultsmodels.BoolStates.YES
bool_states_no = defaultsmodels.BoolStates.NO
bool_states_dict = {'yes':bool_states_yes,'no':bool_states_no}
score_types_tuples_list = defaultsmodels.ScoreTypes.choices#because of "close complaint page"
score_types_dicts = []

#GETTING SCORETYPES CHOICES
for score_type_tuple in score_types_tuples_list:


    score_types_dicts.append({
        'value':score_type_tuple[0],
        'readable':score_type_tuple[1]
    })


def create_complaint_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_company_id = kwargs.get("parameter_company_id")
    company_object = accountsmodels.CustomUser.objects.get(pk=parameter_company_id)

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #check if company is valid
            if company_object:

                #COMPANY INFO

                company_id = company_object.pk
                company_user_type = company_object.user_type
                company_profile = accountsmodels.CompanyProfile.objects.get(user=company_object)
                company_name = company_profile.name
                company_profile_image_url = company_profile.profile_image.url

                #check if company is valid
                if company_user_type == user_types_company:

                    #check if request user is different from the company (cannot complaint to itself, only to others)
                    if company_object != request_user:


                        #GET_DATA

                        company_dict = {'id':company_id,'name':company_name,'profile_image_url':company_profile_image_url}


                        context['GET_data'] ={
                            'company_dict':company_dict
                        }

                        return render(request,'complaints/create_complaint.html',context)

                    else:
                        return HttpResponse("DENIED: same user as company - cannot self complaint")
                else:
                    return HttpResponse("INVALID PARAMETER: not a company id")
            else:
                return HttpResponse("INVALID PARAMETER: company id")
        else:
            return HttpResponse("DENIED: user not authenticated")

    elif request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #check if company is valid
            if company_object:
                
                complaint_form = complaintsforms.CreateComplaintForm(request.POST)

                #check if form is valid
                if complaint_form.is_valid():

                    complaint_title = complaint_form.cleaned_data.get('title')
                    complaint_body = complaint_form.cleaned_data.get('body')

                    complaint_instance = complaintsmodels.ComplaintPost.objects.create(
                        author=request_user,
                        company=company_object,
                        title=complaint_title,
                        body=complaint_body
                    )
                    complaint_instance.save()
                    complaint_instance_id = complaint_instance.pk

                    print("==========================================================")
                    print(f"{complaint_title}_________Complaint created!")
                    print("==========================================================")

                    return redirect('read_complaint',parameter_complaint_id=complaint_instance_id)

                else:
                    print("==========================================================")
                    print("INVALID FORM!")
                    print("==========================================================")

                    return redirect('create_complaint',parameter_company_id=parameter_company_id)

            else:
                return HttpResponse("INVALID PARAMETER: Company id")
        else:
            return HttpResponse("DENIED: user not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def read_complaint_view(request, *args, **kwargs):

    context = {}
    comment_dicts = []
    sorted_comment_dicts = []

    request_user = request.user

    is_authenticated = bool_states_no
    is_author = bool_states_no
    is_company = bool_states_no
    is_comment = bool_states_no

    parameter_complaint_id = kwargs.get("parameter_complaint_id")
    complaint_object = complaintsmodels.ComplaintPost.objects.get(pk=parameter_complaint_id)


    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            is_authenticated = bool_states_yes
            request_user_id = request_user.pk

        #user is not authenticated
        else:
            pass


        #check if complaint is valid
        if complaint_object:


            #COMPLAINT INFO

            complaint_title = complaint_object.title
            complaint_body = complaint_object.body
            complaint_date_created = complaint_object.date_created
            complaint_is_active = complaint_object.is_active
            complaint_is_solved = complaint_object.is_solved
            complaint_score_type = complaint_object.score_type
            complaint_Score_type_readable = ""



            #Maybe fix this loop. Maybe a "while loop" would better

            for score_type_tuple in score_types_tuples_list:

                if score_type_tuple[0] == complaint_score_type:
                    complaint_Score_type_readable = score_type_tuple[1]
                else:
                    pass


            #AUTHOR INFO

            author_object = complaint_object.author
            author_id = complaint_object.pk
            author_user_type = author_object.user_type


            #CHECK IF REQUEST USER IS EITHER AUTHOR/COMPANY OF THE COMPLAINT

            #check if both author and request user are the same
            if request_user == author_object:

                is_author = bool_states_yes

            else:
                #check if both company and request user are the same person
                if request_user == company_object:

                    is_company = bool_states_yes

                #Just a regular user reading the complaint
                else:
                    pass


            #GET AUTHOR NAME

            #check if author is a customer
            if author_object_user_type == user_types_customer:

                author_profile = accountsmodels.CustomerProfile.objects.get(user=author_object)
                author_name = author_profile.first_name + "_" + author_profile.last_name

            #author is a company
            else:

                author_profile = accountsmodels.CompanyProfile.objects.get(user=author_object)
                author_name = author_profile.name

            author_profile_image_url = author_profile.profile_image.url


            #COMPANY INFO

            company_object = complaint_object.company
            company_id = company_object.pk
            company_profile = accountsmodels.CompanyProfile.objects.get(user=company_object)
            company_profile_image_url = company_profile.profile_image.url
            company_name = company_profile.name


            #COMMENTS

            comment_objects = complaintsmodels.ComplaintComment.objects.filter(complaint_post=complaint_object)

            #check for comments
            if comment_objects:

                is_comment = bool_states_yes

                for comment_object in comment_objects:

                    comment_id = comment_object.pk
                    comment_body = comment_object.body
                    comment_date_created = comment_object.date_created

                    comment_author = comment_object.author
                    comment_author_id = comment_author.pk
                    comment_author_user_type = comment_author.user_type

                    #check if author is a customer
                    if comment_author_user_type == user_types_customer:

                        comment_author_profile = accountsmodels.CustomerProfile.objects.get(user=comment_author)
                        comment_author_name = author_profile.first_name + "_" + author_profile.last_name

                    #author is a company
                    else:

                        comment_author_profile = accountsmodels.CompanyProfile.objects.get(user=comment_author)
                        comment_author_name = author_profile.name

                    comment_author_profile_image_url = comment_author_profile.profile_image.url


                    comment_dicts.append({
                        'id':comment_id,
                        'body':comment_body,
                        'date_created':comment_date_created,
                        'author':{'id':comment_author_id,'name':comment_author_name,'profile_image_url':comment_author_profile_image_url}
                    })

                #To sort comments by date_created
                sorted_comment_dicts = sorted(comment_dicts, key=lambda x: x.date_created, reverse=False)

            #No comments
            else:
                pass



            #GET_DATA

            author_dict = {'id':author_id,'name':author_name,'profile_image_url':author_profile_image_url}

            company_dict = {'id':company_id,'name':company_name,'profile_image_url':company_profile_image_url}

            complaint_dict = {'id':parameter_complaint_id,'title':complaint_title,'body':complaint_body,'score_type':complaint_score_type,'date_created':complaint_date_created,'is_active':complaint_is_active,'is_solved':complaint_is_solved}

            comment_dicts = {'is_comment':is_comment,'dicts':sorted_comment_dicts}

            user_dict = {'id':request_user_id,'is_author':is_author,'is_company':is_company,'is_authenticated':is_authenticated}

            defaults_dict = {'bool_states_dict':bool_states_dict,'score_types_dicts':score_types_dicts}


            context['GET_data']={
                'author_dict':author_dict,
                'company_dict':company_dict,
                'complaint_dict':complaint_dict,
                'user_dict':user_dict,
                'comment_dicts':comment_dicts,
                'defaults_dict':defaults_dict
            }


            return render(request, "complaints/read_complaint.html",context)

        else:
            return HttpResponse("INVALID PARAMETER: complaint id")
    else:
        return HttpResponse("INVALID REQUEST!")



def update_complaint_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_complaint_id = kwargs.get("parameter_complaint_id")
    complaint_object = complaintsmodels.ComplaintPost.objects.get(pk=parameter_complaint_id)


    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                complaint_title = complaint_object.title
                complaint_body = complaint_object.body
                complaint_is_active = complaint_object.is_active


                author_object = complaint_object.author

                #check if both author and request users are the same person
                if request_user == author_object:

                    #check if complaint is open
                    if complaint_is_active == bool_states_yes:


                        #GET_DATA

                        complaint_dict = {'id':parameter_complaint_id,'title':complaint_title,'body':complaint_body}


                        context['GET_data'] ={
                            'complaint_dict':complaint_dict
                        }


                        return render(request, "complaints/update_complaint.html",context)

                    else:
                        return HttpResponse("DENIED: cannot update a closed complaint")
                else:
                    return HttpResponse("DENIED: cannot update other users's complaints")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: User is not authenticated")


    elif request.method == 'POST':

         #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                author_object = complaint_object.author

                #check if both author and request users are the same person
                if request_user == author_object:

                    #check if complaint is open/closed
                    if complaint_is_active == bool_states_yes:

                        complaint_form = complaintsforms.UpdateComplaintForm(request.POST,instance=complaint_object)

                        if complaint_form.is_valid():

                            complaint_form.save()

                            return redirect('read_complaint',parameter_complaint_id=parameter_complaint_id)

                        else:
                            print("==========================================================")
                            print("INVALID FORM!")
                            print("==========================================================")
                            return redirect('update_complaint',parameter_complaint_id=parameter_complaint_id)

                    else:
                        return HttpResponse("DENIED: cannot update closed complaint")
                else:
                    return HttpResponse("DENIED: cannot update other users's complaints")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def delete_complaint_view(request,*args, **kwargs):

    context = {}
    request_user = request.user

    parameter_complaint_id = kwargs.get("parameter_complaint_id")
    complaint_object = complaintsmodels.ComplaintPost.objects.get(pk=parameter_complaint_id)


    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                complaint_title = complaint_object.title

                author_object = complaint_object.author

                #check if both author and request users are the same person
                if request_user == author_object:


                    #GET_DATA

                    complaint_dict = {'id':parameter_complaint_id,'title':complaint_title}


                    context['GET_data'] ={
                        'complaint_dict':complaint_dict
                    }


                    return render(request, "complaints/delete_complaint.html",context)

                else:
                    return HttpResponse("DENIED: cannot delete other users's complaint")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: user is not authenticated")


    elif request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                author_object = complaint_object.author

                #check if both author and request users are the same person
                if request_user == author_object:

                    complaint_object.delete()

                    print("==========================================================")
                    print("Complaint deleted!")
                    print("==========================================================")
                    return redirect("home_page")

                else:
                    return HttpResponse("DENIED: cannot delete other users's complaints")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def close_complaint_view(request,*args, **kwargs):

    context = {}

    request_user = request.user
    
    parameter_complaint_id = kwargs.get("parameter_complaint_id")
    complaint_object = complaintsmodels.ComplaintPost.objects.get(pk=parameter_complaint_id)


    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                #Complaint info

                complaint_title = complaint_object.title
                complaint_is_active = complaint_object.is_active


                #Author info

                author_object = complaint_object.author


                #check if both author and request users are the same person
                if request_user == author_object:

                    #check if complaint is open
                    if complaint_is_active == bool_states_yes:



                        #GET_DATA

                        complaint_dict = {'id':parameter_complaint_id,'title':complaint_title}
                        defaults_dict = {'score_types_dicts':score_types_dicts}

                        context['GET_data'] ={
                            'complaint_dict':complaint_dict,
                            'defaults_dict':defaults_dict
                        }

                        return render(request, "complaints/close_complaint.html",context)

                    else:
                        return HttpResponse("DENIED: complaint is already closed")
                else:
                    return HttpResponse("DENIED: cannot close other users's complaints")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: user is not authenticated")


    elif request.method == 'POST':

         #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                #Complaint info
                complaint_is_active = complaint_object.is_active

                #Author
                author_object = complaint_object.author


                #check if both author and request users are the same person
                if request_user == author_object:

                    #check if complaint is open/closed
                    if complaint_is_active == bool_states_yes:

                        complaint_form = complaintsforms.CloseComplaintForm(request.POST,instance=complaint_object)

                        if complaint_form.is_valid():

                            #Save complaint instance by updating is_ative field
                            complaint_instance = complaint_form.save(commit=False)
                            complaint_instance.is_active = bool_states_no
                            complaint_instance.save()

                            return redirect('read_complaint',parameter_complaint_id=parameter_complaint_id)

                        else:
                            print("==========================================================")
                            print("INVALID FORM!")
                            print("==========================================================")

                            return redirect('close_complaint',parameter_complaint_id=parameter_complaint_id)

                    else:
                        return HttpResponse("DENIED: complaint is already closed")
                else:
                    return HttpResponse("DENIED: cannot close other users's complaints")
            else:
                return HttpResponse("INVALID PARAMETER: complaint id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def user_complaint_list_view(request):

    context = {}
    complaint_dicts = []
    sorted_complaint_dicts = []

    request_user = request.user

    is_complaint = bool_states_no

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            complaint_objects = complaintsmodels.ComplaintPost.objects.filter(author=request_user)

            #check if user has created complaints
            if complaint_objects:

                is_complaint = bool_states_yes

                for complaint_object in complaint_objects:

                    complaint_id = complaint_object.pk
                    complaint_title = complaint_object.title

                    complaint_dicts.append({'id':complaint_id,'title':complaint_title})

                sorted_complaint_dicts = sorted(complaint_dicts, key=lambda x: x.title, reverse=False)

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


            return render(request, "complaints/user_complaint_list.html",context)

        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def create_comment_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_complaint_id = kwargs.get("parameter_complaint_id")
    complaint_object = complaintsmodels.ComplaintComment.objects.get(pk=parameter_complaint_id)

    if request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #check if complaint is valid
            if complaint_object:

                author_object = complaint_object.author
                company_object = complaint_object.company
                complaint_is_active = complaint_object.is_active

                #check if user is either complaint author or comapny
                if request_user == author_object or request_user == company_object:

                    #check if complaint is open
                    if complaint_is_active == bool_states_yes:

                        comment_form = complaintsforms.CreateCommentForm(request.POST)

                        #check if form is valid
                        if comment_form.is_valid():

                            comment_body = comment_form.cleaned_data.get('body')

                            comment_instance = complaintsmodels.ComplaintComment.objects.create(
                                author=request_user,
                                complaint_post=complaint_object,
                                body=comment_body
                            )

                            comment_instance.save()

                            print("==========================================================")
                            print("Comment created!")
                            print("==========================================================")
                        else:
                            print("==========================================================")
                            print("INVALID FORM!")
                            print("==========================================================")

                        return redirect('read_complaint',parameter_complaint_id=parameter_complaint_id)

                    else:
                        return HttpResponse("DENIED: cannot create comment because complaint is already closed")
                else:
                    return HttpResponse("DENIED: you cannot comment on this complaint")
            else:
                return HttpResponse("INVALID PARAMETER: company id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def update_comment_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_comment_id = kwargs.get("parameter_comment_id")
    comment_object = complaintsmodels.ComplaintComment.objects.get(pk=parameter_comment_id)


    if request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #check if comment is valid
            if comment_object:

                author_object = comment_object.author
                complaint_object = comment_object.complaint_post
                complaint_object_id = complaint_object.pk
                complaint_is_active = complaint_object.is_active

                #check if user is author
                if request_user == parameter_comment_author:

                    #check if complaint is open
                    if complaint_is_active == bool_states_yes:

                        comment_form = complaintsforms.UpdateCommentForm(request.POST,instance=comment_object)

                        #check if form is valid
                        if comment_form.is_valid():

                            comment_form.save()

                            print("==========================================================")
                            print("Comment Updated!")
                            print("==========================================================")
                        else:
                            print("==========================================================")
                            print("INVALID FORM!")
                            print("==========================================================")


                        return redirect('read_complaint',parameter_complaint_id=complaint_object_id)

                    else:
                        return HttpResponse("DENIED: cannot update comment because complaint is already closed")
                else:
                    return HttpResponse("DENIED: cannot update other users's comment")
            else:
                return HttpResponse("INVALID PARAMETER: comment id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")
