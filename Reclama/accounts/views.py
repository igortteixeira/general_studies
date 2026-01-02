from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout

#REST FRAMEWORK
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

#Personalized imports
import accounts.models as accountsmodels
import accounts.forms as accountsforms
import defaults.models as defaultsmodels


#CONST_VARIABLES
object_types_dict = {'user':object_types_user,'complaint':object_types_complaint}
user_types_dict = {'customer':user_types_customer,'company':user_types_company}


@api_view(['POST','GET'])
def create_customer_view(request):

    customer_dict = {}
    defaults_dict = {}

    if request.method == 'GET':

        #GET_data

        defaults_dict = {'user_types_dict':user_types_dict}

        GET_data={
            'defaults_dict':defaults_dict,
            'message':{'SUCCESS': 'Create Customer Page'}

        }

        #Converting response data into json
        context = JSONRenderer().render(GET_data)

        return Response(context,status=status.HTTP_200_OK)

    else:

        if request.method == 'POST':

            #POST_data

            request_data_converted = JSONParser().parse(request_data)
            print(request_data_converted)

            POST_data={
                'customer_dict':request_data_converted,
                'message':{'SUCCESS': 'Data Submitted!'}
            }

            #Converting response data into json
            context = JSONRenderer().render(POST_data)

            return Response(context,status=status.HTTP_200_OK)
        
        else:

            #RESPONSE_data

            request_reponse={
                'message':{'FAILED': 'Invalid request type'}
            }
            context = JSONRenderer().render(request_reponse)

            return Response(context,status=status.HTTP_400_BAD_REQUEST)



def logout_user_view(request):

    context = {}
    user_dict = {}

    request_user = request.user

    if request.method == 'GET':

        #check if user is authenticated
        if request_user.is_authenticated:

            request_user_username = request_user.username


            #GET_DATA

            user_dict = {'username':request_user_username}

            context['GET_data']={
                'user_dict':user_dict
            }

            return render(request, "accounts/logout.html",context)

        else:
            return HttpResponse("DENIED: user is not authenticated")

    elif request.method == 'POST':

        #check if user is authenticated
        if request_user.is_authenticated:

            logout(request)
            print("==========================================================")
            print("LOGGED OUT!")
            print("==========================================================")

            return redirect('home_page')

        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def user_profile_view(request, *args, **kwargs):

    context = {}
    user_profile_dict = {}
    user_dict = {}
    defaults_dict = {}

    request_user = request.user
    path_name = request.resolver_match.view_name#for_favorite_feature
    is_self = bool_states_no

    is_favorite = bool_states_no
    favorite_id = bool_states_no


    parameter_user_id = kwargs.get("parameter_user_id")
    parameter_user = accountsmodels.CustomUser.objects.get(pk=parameter_user_id)

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #REQUEST USER INFO

            request_user_id = request_user.pk
            request_user_username = request_user.username
            request_user_user_type = request_user.user_type

            #check if parameter_user is valid/exists
            if parameter_user:

                parameter_user_user_type = parameter_user.user_type

                #check if both parameter and request users are the same person
                if request_user == parameter_user:
                    is_self = bool_states_yes

                    #check if user type is CUSTOMER
                    if request_user_user_type == user_types_customer:

                        #CUSTOMER PROFILE

                        request_user_profile = accountsmodels.CustomerProfile.objects.get(user=request_user)

                        request_user_profile_name = request_user_profile.name
                        request_user_profile_profile_image_url = request_user_profile.profile_image.url

                        user_profile_dict = {
                            'name':request_user_profile_name,
                            'profile_image_url':request_user_profile_profile_image_url
                        }


                    #COMPANY PROFILE
                    else:

                        request_user_profile = accountsmodels.CompanyProfile.objects.get(user=request_user)

                        request_user_profile_name = request_user_profile.name
                        request_user_profile_description = request_user_profile.description
                        request_user_profile_location = request_user_profile.location
                        request_user_profile_phone_number = request_user_profile.phone_number
                        request_user_profile_profile_image_url = request_user_profile.profile_image.url

                        user_profile_dict = {
                            'name':request_user_profile_name,
                            'description':request_user_profile_description,
                            'location':request_user_profile_location,
                            'phone_number':request_user_profile_phone_number,
                            'profile_image_url':request_user_profile_profile_image_url
                        }

                    user_dict = {
                        'id':request_user_id,
                        'is_self':is_self,
                        'username':request_user_username,
                        'user_type':request_user_user_type,
                        'profile_dict':user_profile_dict
                    }


                #user is not self
                else:
                    
                    #check if parameter user is CUSTOMER
                    if parameter_user_user_type == user_types_customer:

                        #CUSTOMER PROFILE

                        parameter_user_profile = accountsmodels.CustomerProfile.objects.get(user=parameter_user)

                        parameter_user_profile_name = parameter_user_profile.name
                        parameter_user_profile_profile_image_url = parameter_user_profile.profile_image.url


                        user_profile_dict = {
                            'name':parameter_user_profile_name,
                            'profile_image_url':parameter_user_profile_profile_image_url
                        }
                    
                    #COMPANY profile 
                    else:

                        parameter_user_profile = accountsmodels.CompanyProfile.objects.get(user=parameter_user)

                        parameter_user_profile_name = parameter_user_profile.name
                        parameter_user_profile_description = parameter_user_profile.description
                        parameter_user_profile_location = parameter_user_profile.location
                        parameter_user_profile_phone_number = parameter_user_profile.phone_number
                        parameter_user_profile_profile_image_url = parameter_user_profile.profile_image.url


                        #Check if company is favorite

                        #fix - must confirm single result
                        favorite_company_object = homemodels.Favorites.objects.filter(user=request_user,foreign_int=parameter_user_id,object_type=object_types_user)

                        if favorite_company_object:

                            favorite_company_object = favorite_company_object[0]
                            is_favorite = bool_states_yes
                            favorite_id = favorite_company_object.pk

                        else:

                            is_favorite = bool_states_no


                        user_profile_dict = {
                            'name':parameter_user_profile_name,
                            'description':parameter_user_profile_description,
                            'location':parameter_user_profile_location,
                            'phone_number':parameter_user_profile_phone_number,
                            'profile_image_url':parameter_user_profile_profile_image_url
                        }

                    user_dict = {
                        'id':parameter_user_id,
                        'is_self':is_self,
                        'user_type':parameter_user_user_type,
                        'profile_dict':user_profile_dict,
                        'is_favorite':is_favorite,
                        'favorite_id':favorite_id,
                        'object_type':object_types_user
                    }



                #GET_DATA


                defaults_dict = {'user_types_dict':user_types_dict,'bool_states_dict':bool_states_dict}

                page_dict = {'path_name':path_name}


                context['GET_data']={
                    'user_dict':user_dict,
                    'defaults_dict':defaults_dict,
                    'page_dict':page_dict
                }

                return render(request, "accounts/user_profile.html",context)

            else:
                return HttpResponse("INVALID PARAMETER: user id")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")



def update_profile_view(request, *args, **kwargs):

    context = {}

    request_user = request.user

    if request.method == 'GET':

        #check if user is logged
        if request_user.is_authenticated:

            #REQUEST USER INFO

            request_user_id = request_user.pk
            request_user_username = request_user.username
            request_user_user_type = request_user.user_type

            #check if user type is CUSTOMER
            if request_user_user_type == user_types_customer:

                #CUSTOMER INFO

                request_user_profile = accountsmodels.CustomerProfile.objects.get(user=request_user)

                request_user_profile_name = request_user_profile.name
                request_user_profile_image_url = request_user_profile.profile_image.url

                profile_dict = {
                    'name':request_user_profile_name,
                    'profile_image_url':request_user_profile_image_url
                }


            #COMPANY PROFILE
            else:
                request_user_profile = accountsmodels.CompanyProfile.objects.get(user=request_user)

                request_user_profile_name = request_user_profile.name
                request_user_profile_description = request_user_profile.description
                request_user_profile_location = request_user_profile.location
                request_user_profile_phone_number = request_user_profile.phone_number
                request_user_profile_image_url = request_user_profile.profile_image.url

                profile_dict = {
                    'name':request_user_profile_name,
                    'description':request_user_profile_description,
                    'location':request_user_profile_location,
                    'phone_number':request_user_profile_phone_number,
                    'profile_image_url':request_user_profile_image_url
                }



            #GET_DATA

            defaults_dict = {'user_types_dict':user_types_dict}

            user_dict = {
                'id':request_user_id,
                'username':request_user_username,
                'user_type':request_user_user_type,
                'profile_dict':profile_dict
            }


            context['GET_data']={
                'user_dict':user_dict,
                'defaults_dict':defaults_dict
            }



            return render(request, "accounts/update_profile.html",context)

        else:
            return HttpResponse("DENIED: user is not authenticated")

    elif request.method == 'POST':

        #check if user is logged
        if request_user.is_authenticated:

            request_user_id = request_user.pk
            request_user_user_type = request_user.user_type

            #check if user type is CUSTOMER
            if request_user_user_type == user_types_customer:

                request_user_profile = accountsmodels.CustomerProfile.objects.get(user=request_user)
                form_object = accountsforms.UpdateCustomerProfileForm(request.POST,request.FILES,instance=request_user_profile)

            #COMPANY PROFILE
            else:

                request_user_profile = accountsmodels.CompanyProfile.objects.get(user=request_user)
                form_object = accountsforms.UpdateCompanyProfileForm(request.POST,request.FILES,instance=request_user_profile)

            if form_object.is_valid():

                form_object.save()

                return redirect('user_profile_page', parameter_user_id=request_user_id)

            else:
                print("==========================================================")
                print("INVALID FORM!")
                print("==========================================================")
                
                return redirect("update_profile_page")
        else:
            return HttpResponse("DENIED: user is not authenticated")
    else:
        return HttpResponse("INVALID REQUEST!")





def users_list_view(request):

    context = {}
    user_dicts_list = []

    is_user = bool_states_no

    if request.method == 'GET':

        user_objects = accountsmodels.CustomUser.objects.all()

        if user_objects:

            is_user = bool_states_yes

            for user_object in user_objects:

                user_object_id = user_object.pk
                user_object_user_type = user_object.user_type

                if user_object_user_type == user_types_customer:

                    user_object_profile = accountsmodels.CustomerProfile.objects.get(user=user_object)

                else:

                    user_object_profile = accountsmodels.CompanyProfile.objects.get(user=user_object)

                user_object_profile_name = user_object_profile.name
                user_object_profile_image_url = user_object_profile.profile_image.url

                profile_dict = {
                    'name':user_object_profile_name,
                    'profile_image_url':user_object_profile_image_url
                }

                user_dict = {
                    'id':user_object_id,
                    'user_type':user_object_user_type,
                    'profile_dict':profile_dict
                }

                user_dicts_list.append(user_dict)

        #No results
        else:
            is_user = bool_states_no

        #GET_DATA

        user_dicts = {'is_user':is_user,'dicts':user_dicts_list}

        defaults_dict = {'bool_states_dict':bool_states_dict,'user_types_dict':user_types_dict}

        

        context['GET_data'] ={
            'user_dicts':user_dicts,
            'defaults_dict':defaults_dict
        }


        return render(request, "accounts/users_list.html",context)
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

                    favorite_objects_list.append({'id':favorite_id,'object_id':object_id,'object_type':object_type})

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
