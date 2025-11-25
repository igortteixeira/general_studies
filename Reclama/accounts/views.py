from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout

import accounts.models as accountsmodels
import accounts.forms as accountsforms
import defaults.models as defaultsmodels
import home.models as homemodels


#ENV_VARIABLES
user_types_company = defaultsmodels.UserTypes.COMPANY
user_types_customer = defaultsmodels.UserTypes.CUSTOMER
bool_states_yes = defaultsmodels.BoolStates.YES
bool_states_no = defaultsmodels.BoolStates.NO
object_types_user = defaultsmodels.ObjectTypes.USER
object_types_complaint = defaultsmodels.ObjectTypes.COMPLAINT
object_types_dict = {'user':object_types_user,'complaint':object_types_complaint}
user_types_dict = {'customer':user_types_customer,'company':user_types_company}
bool_states_dict = {'yes':bool_states_yes,'no':bool_states_no}



def choose_user_type_view(request):

    context = {}
    defaults_dict = {}

    #variable "declaration/initialization"
    '''
    '''

    request_user = request.user

    if request.method == 'GET':

        #check if user is not already logged
        if not request_user.is_authenticated:


            #GET_DATA

            defaults_dict = {'user_types_dict':user_types_dict}


            context['GET_data']={
                'defaults_dict':defaults_dict
            }

            return render(request,'accounts/choose_user_type.html',context)

        else:
            return HttpResponse("DENIED: user is authenticated")


    elif request.method == 'POST':

        #check if user is not already logged
        if not request_user.is_authenticated:

            user_type_form = accountsforms.ChooseUserTypeForm(request.POST)

            #check if form is valid
            if user_type_form.is_valid():

                user_type = user_type_form.cleaned_data.get('user_type')

                return redirect('create_user_page',user_type_choice=user_type)

            else:
                print("==========================================================")
                print("INVALID FORM!")
                print("==========================================================")

                return redirect('choose_user_type_page')
        else:
            return HttpResponse("DENIED: user is authenticated already")
    else:
        return HttpResponse("INVALID REQUEST!")



def create_user_view(request,*args, **kwargs):

    context = {}
    user_dict = {}
    defaults_dict = {}

    #variable "declaration/initialization"
    '''
    request_user_instance = None
    username = None
    user_type = None
    profile_image = None
    first_name = None
    last_name = None
    name = None
    description = None
    location = None
    phone_number = None
    profile_instance = None
    '''

    request_user = request.user

    user_type_choice = kwargs.get("user_type_choice")

    if request.method == 'GET':

        #check if user type is valid
        if user_type_choice == user_types_customer or user_type_choice == user_types_company:

            #check if user is not already logged
            if not request_user.is_authenticated:


                #GET_DATA

                user_dict = {'user_type_choice':user_type_choice}

                defaults_dict = {'user_types_dict':user_types_dict}



                context['GET_data']={
                    'user_dict':user_dict,
                    'defaults_dict':defaults_dict
                }

                return render(request,'accounts/create_user.html',context)

            else:
                return HttpResponse("DENIED: user is authenticated")
        else:
            return HttpResponse("INVALID PARAMETER: user type")

    elif request.method == 'POST':

        #check if user is not already logged
        if not request_user.is_authenticated:

            #check if user type is valid
            if user_type_choice == user_types_customer or user_type_choice == user_types_company:

                #check if user type is CUSTOMER
                if user_type_choice == user_types_customer:

                    user_form = accountsforms.CreateUserForm(request.POST)
                    profile_form = accountsforms.CreateCustomerProfileForm(request.POST,request.FILES)

                    #check if both user and profile forms are valid
                    if user_form.is_valid() and profile_form.is_valid():

                        request_user_instance = user_form.save(commit=False)

                        request_user_instance.user_type = user_types_customer
                        request_user_instance.save()

                        username = request_user_instance.username
                        user_type = request_user_instance.user_type

                        profile_image = profile_form.cleaned_data.get('profile_image')
                        profile_name = profile_form.cleaned_data.get('name')

                        
                        #CHECK FOR BLANK FIELDS

                        if not profile_name:
                            profile_name = 'Undefined Name'
                        else:
                            pass


                        profile_instance = accountsmodels.CustomerProfile.objects.create(
                            user=request_user_instance,
                            name=profile_name,
                            profile_image=profile_image
                        )


                        print("==========================================================")
                        print(f"{user_type} created!")
                        print({"username":username,"Name":profile_name})
                        print("==========================================================")

                    else:
                        print("==========================================================")
                        print("INVALID FORM!")
                        print("==========================================================")

                        return redirect('create_user_page',user_type_choice=user_type_choice)


                #user type COMPANY
                else:

                    user_form = accountsforms.CreateUserForm(request.POST)
                    profile_form = accountsforms.CreateCompanyProfileForm(request.POST,request.FILES)

                    #check if both user and profile forms are valid
                    if user_form.is_valid() and profile_form.is_valid():

                        request_user_instance = user_form.save(commit=False)
                        
                        request_user_instance.user_type = user_types_company
                        request_user_instance.save()

                        #CHECK FOR BLANK FIELDS

                        optional_company_fields = ('name')

                        profile_image = profile_form.cleaned_data.get('profile_image')
                        profile_name = profile_form.cleaned_data.get('name')
                        profile_description = profile_form.cleaned_data.get('description')
                        profile_location = profile_form.cleaned_data.get('location')
                        profile_phone_number = profile_form.cleaned_data.get('phone_number')


                        #CHECK FOR BLANK FIELDS (Maybe could improve it)

                        if not profile_name:
                            profile_name = 'Undefined Name'
                        else:
                            pass

                        if not profile_description:
                            profile_description = 'Undefined Description'
                        else:
                            pass

                        if not profile_location:
                            profile_location = 'Undefined Location'
                        else:
                            pass

                        if not profile_phone_number:
                            profile_phone_number = 'Undefined Phone Number'
                        else:
                            pass


                        profile_instance = accountsmodels.CompanyProfile.objects.create(
                            user=request_user_instance,
                            name=profile_name,
                            description=profile_description,
                            location=profile_location,
                            phone_number=profile_phone_number,
                            profile_image=profile_image
                        )
                                                                                                                                                                                                
                    else:
                        print("==========================================================")
                        print("INVALID FORM!")
                        print("==========================================================")

                        return redirect('create_user_page',user_type_choice=user_type_choice)

                profile_instance.save()

                username = request_user_instance.username
                user_type = request_user_instance.user_type

                print("==========================================================")
                print(f"{user_type} created!")
                print({"username":username,"name":profile_name})
                print("==========================================================")

                return redirect('login_page')

            else:
                return HttpResponse("INVALID PARAMETER: user type")
        else:
            return HttpResponse("DENIED: user is authenticated already")
    else:
        return HttpResponse("INVALID REQUEST!")



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


