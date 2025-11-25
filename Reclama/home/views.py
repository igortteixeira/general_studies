from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

import accounts.models as accountsmodels
import complaints.models as complaintsmodels
import home.models as homemodels
import defaults.models as defaultsmodels


#ENV_VARIABLES
object_types_user = defaultsmodels.ObjectTypes.USER
object_types_complaint = defaultsmodels.ObjectTypes.COMPLAINT
user_types_company = defaultsmodels.UserTypes.COMPANY
user_types_customer = defaultsmodels.UserTypes.CUSTOMER
object_types_dict = {'user':object_types_user,'complaint':object_types_complaint}
bool_states_yes = defaultsmodels.BoolStates.YES
bool_states_no = defaultsmodels.BoolStates.NO
bool_states_dict = {'yes':bool_states_yes,'no':bool_states_no}


def home_view(request):
    
    context = {}

    request_user = request.user

    is_authenticated = bool_states_no

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            is_authenticated = bool_states_yes
            request_user_id = request_user.pk

        #user is not authenticated
        else:
            request_user_id = bool_states_no



        #GET_DATA

        defaults_dict = {'bool_states_dict':bool_states_dict}

        user_dict = {'id':request_user_id,'is_authenticated':is_authenticated}


        context['GET_data']={
            'user_dict':user_dict,
            'defaults_dict':defaults_dict
        }


        return render(request,'home/home.html',context)

    else:
        return HttpResponse("INVALID REQUEST!")



def searching_view(request, *args, **kwargs):

    if request.method == 'GET':

        context = {}
        filter_results = []
        sorted_filter_results = []

        is_result = bool_states_no

        parameter_search_string = request.GET.get("parameter_search_string")

        #if user passed some arguments
        if parameter_search_string:

            company_results = accountsmodels.CompanyProfile.objects.filter(name__icontains=parameter_search_string)
            complaint_results = complaintsmodels.ComplaintPost.objects.filter(title__icontains=parameter_search_string)

            #check if there's company or complaint results
            if company_results or complaint_results:

                is_result = bool_states_yes

                #if there's company results
                if company_results:

                    for company in company_results:

                        #company info

                        company_object = company.user
                        company_id = company_object.id
                        company_name = company.name

                        filter_results.append({'id':company_id,'name':company_name,'object_type':object_types_user})

                #no company results
                else:
                    pass

                #if there's complaint results
                if complaint_results:

                    for complaint in complaint_results:

                        #complaint info

                        complaint_id = complaint.pk
                        complaint_title = complaint.title

                        filter_results.append({'id':complaint_id,'name':complaint_title,'object_type':object_types_complaint})

                #No complaint results
                else:
                    pass

                sorted_filter_results = sorted(filter_results, key=lambda x: x['name'], reverse=False)

            #No results
            else:
                pass

        #No arguments
        else:
            pass

        #GET Data

        search_result_dicts = {'is_result':is_result,'dicts':sorted_filter_results}

        defaults_dict = {'object_types_dict':object_types_dict,'bool_states_dict':bool_states_dict}


        context['GET_data']={

            'search_result_dicts':search_result_dicts,
            'defaults_dict':defaults_dict
        }

        return render(request,'home/searching.html',context)

    else:
        return HttpResponse("INVALID REQUEST!")



def favorite_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_object_type = kwargs.get("parameter_object_type")
    parameter_object_id = kwargs.get("parameter_object_id")
    parameter_path_name = kwargs.get("parameter_path_name")

    if request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #VALIDATE object_id

            #check if object_type is valid
            if parameter_object_type == object_types_complaint or parameter_object_type == object_types_user:

                #check if it's a complaint post
                if parameter_object_type == object_types_complaint:

                    #fix - must confirm single result
                    parameter_object = complaintsmodels.ComplaintPost.objects.filter(pk=parameter_object_id)


                #check if it's company user
                else:

                    #fix - must confirm single result
                    parameter_object = accountsmodels.CustomUser.objects.filter(pk=parameter_object_id,user_type=user_types_company)


                #check if parameter object is valid
                if parameter_object:

                    #fix - must confirm single result
                    parameter_object = parameter_object[0]

                    #fix - must confirm single result
                    favorite_object = homemodels.Favorites.objects.filter(pk=parameter_object_id)

                    #Check if complaint is not already favorite
                    if not favorite_object:

                        favorite_instance = homemodels.Favorites.objects.create(
                            user=request_user,
                            foreign_int=parameter_object_id,
                            object_type=parameter_object_type
                        )

                        favorite_instance.save()

                        print("==========================================================")
                        print("Added to Favorites!")
                        print("==========================================================")


                        #REDIRECT

                        #if post request comes from a complaint page
                        if parameter_path_name == 'read_complaint_page':

                            return redirect('read_complaint_page',parameter_complaint_id=parameter_object_id)

                        else:

                            #if post request comes from a company page
                            if parameter_path_name == 'user_profile_page':

                                return redirect('user_profile_page', parameter_user_id=parameter_object_id)

                            else:

                                #if post request comes from user favorite list
                                if parameter_path_name == 'user_favorite_list_page':

                                    return redirect('user_favorite_list_page')

                                else:

                                    #just redirect to home page
                                    return redirect('home_page')



                    else:
                        return HttpResponse("DENIED: already favorite")
                else:
                    return HttpResponse("INVALID PARAMETER: object id")
            else:
                return HttpResponse("INVALID PARAMETER: object type")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def unfavorite_view(request,*args, **kwargs):

    context = {}

    request_user = request.user

    parameter_favorite_id = kwargs.get("parameter_favorite_id")
    parameter_redirect_name = kwargs.get("parameter_path_name")

    if request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            #fix - must confirm single result
            favorite_object = homemodels.Favorites.objects.filter(pk=parameter_favorite_id)

            #check if favorite is valid
            if favorite_object:

                favorite_object = favorite_object[0]
                favorite_object_foreign_int = favorite_object.foreign_int
                favorite_object_user = favorite_object.user

                #Check if both request user and favorite's user are the same person
                if request_user == favorite_object_user:

                    favorite_object.delete()

                    print("==========================================================")
                    print("Removed from favorites")
                    print("==========================================================")

                    #REDIRECT

                    #if post request comes from a complaint page
                    if parameter_redirect_name == 'read_complaint_page':

                        return redirect('read_complaint_page',parameter_complaint_id=favorite_object_foreign_int)

                    else:

                        #if post request comes from a company page
                        if parameter_redirect_name == 'user_profile_page':

                            return redirect('user_profile_page', parameter_user_id=favorite_object_foreign_int)

                        else:

                            #if post request comes from user favorite list
                            if parameter_redirect_name == 'user_favorite_list_page':

                                return redirect('user_favorite_list_page')

                            else:

                                #just redirect to home page
                                return redirect('home_page')

                else:
                    return HttpResponse("DENIED: cannot unfavorite other people favorites")
            else:
                return HttpResponse("INVALID PARAMETER: favorite id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def user_favorite_list_view(request):

    context = {}
    favorite_objects_list = []

    path_name = request.resolver_match.view_name
    request_user = request.user

    is_result = bool_states_no

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            favorite_objects = homemodels.Favorites.objects.filter(user=request_user)

            #check is results
            if favorite_objects:

                is_result = bool_states_yes

                for result in favorite_objects:

                    favorite_id = result.pk
                    object_id = result.foreign_int
                    object_type = result.object_type
                    object_name = result.name
                    object_title = result.title
                    object_image_url = result.company_profile_image_url

                    favorite_objects_list.append({'id':favorite_id,'object_id':object_id,'name':object_name,'title':object_title,'profile_image_url':object_image_url,'object_type':object_type})

            #No results
            else:
                pass



            #GET Data

            favorite_dicts = {'is_result':is_result,'dicts':favorite_objects_list}

            defaults_dict = {'object_types_dict':object_types_dict,'bool_states_dict':bool_states_dict}

            page_dict = {'path_name':path_name}


            context['GET_data']={

                'favorite_dicts':favorite_dicts,
                'defaults_dict':defaults_dict,
                'page_dict':page_dict
            }


            return render(request, "home/user_favorite_list.html",context)

        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")
