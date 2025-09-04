from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, UpdateProfileForm#,LoginUserForm
from .models import Profile
from friendships.models import FriendRelation,FriendRequest



def create_user_view(request):
    request_user = request.user

    #check if user is not already logged
    if not request_user.is_authenticated:

        if request.method == 'POST':
            user_form = CreateUserForm(request.POST)
            profile_form = UpdateProfileForm(request.POST,request.FILES)

            #check if both user and profile forms are valid
            if user_form.is_valid() and profile_form.is_valid():
                request_user_instance = user_form.save()
                profile_image = profile_form.cleaned_data.get('image')
                profile_instance = Profile.objects.create(user=request_user_instance,image=profile_image)
                profile_instance.save()

                username = user_form.cleaned_data.get('username')
                raw_password = user_form.cleaned_data.get('password1')

                print("==========================================================")
                print("USER CREATED!")
                print(f"Username: {username}, Password:{raw_password}")
                print("==========================================================")

                return redirect('login_page')
            else:
                print("==========================================================")
                print("INVALID FORM!")
                print("==========================================================")
                return redirect('create_user_page')

        elif request.method == 'GET':
            return render(request, 'accounts/create_user.html')

        else:
            return HttpResponse("INVALID REQUEST!")
    else:
        return HttpResponse("LOGOUT REQUIRED!")

'''
def login_user_view(request):
    request_user = request.user
    if request_user.is_authenticated:
        return HttpResponse("LOGOUT REQUIRED!")
    else:
        if request.method == 'POST':
            user_form = LoginUserForm(request.POST)
            if user_form.is_valid():
                try:
                    username = user_form.cleaned_data.get('username').lower()
                    raw_password = user_form.cleaned_data.get('password')
                    account = authenticate(username=username, password=raw_password)
                    login(request, account)

                    print("==========================================================")
                    print("LOGGED!")
                    print("==========================================================")
                    return redirect("home_page")
                except:
                    print("==========================================================")
                    print("LOGIN ERROR!")
                    print("==========================================================")
                    return redirect('login_page')
            else:
                print("==========================================================")
                print("INVALID FORM!")
                print("==========================================================")
                return redirect('login_page')
        elif request.method == 'GET':
            return render(request, "accounts/login.html")
        else:
            return HttpResponse("INVALID REQUEST!")
'''

def logout_user_view(request):
    request_user = request.user

    #check if user is authenticated
    if request_user.is_authenticated:
        
        if request.method == 'POST':

            logout(request)
            print("==========================================================")
            print("LOGGED OUT!")
            print("==========================================================")
            return redirect("home_page")

        elif request.method == 'GET':
            context = {}
            context['username'] = request_user.username
            return render(request, "accounts/logout.html",context)

        else:
            return HttpResponse("INVALID REQUEST!")
    else:
        return HttpResponse("LOGIN REQUIRED!")




def user_profile_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:

        request_user_id = request_user.pk
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if parameter_user_id is valid
        if parameter_user:
            if request.method == 'GET':
                context = {}
                is_self = False
                is_friend = False
                is_requested_friend = False
                is_requesting_friend = False
                parameter_user_profile = Profile.objects.get(user=parameter_user)
                
                #check if both parameter and request users are NOT the same person
                if request_user != parameter_user:

                    #check if parameter user is NOT friend
                    request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
                    if not request_parameter_users_relation:

                        #check if request user made NOT friend request to parameter user
                        request_user_friend_request = FriendRequest.objects.filter(requesting_user=request_user,requested_user=parameter_user)
                        if not request_user_friend_request:

                            #check if parameter user made NOT friend request to request user
                            parameter_user_friend_request = FriendRequest.objects.filter(requesting_user=parameter_user,requested_user=request_user)
                            if not parameter_user_friend_request:

                                is_requested_friend = False
                                is_requesting_friend = False

                            else:
                                is_requesting_friend = True
                        else:
                            is_requested_friend = True
                    else:
                        is_friend = True

                    context['is_friend'] = is_friend
                    context['is_requesting_friend'] = is_requesting_friend
                    context['is_requested_friend'] = is_requested_friend
                    context['user_id'] = parameter_user_id
                    context['username'] = parameter_user.username
                    context['profile_image_src'] = parameter_user_profile.image.url
                    context['is_self'] = is_self


                else:
                    is_self = True
                    request_user_profile = Profile.objects.get(user=request_user)
                    context['user_id'] = request_user_id
                    context['username'] = request_user.username
                    context['profile_image_src'] = request_user_profile.image.url
                    context['is_self'] = is_self


                return render(request, "accounts/user_profile.html",context)
            else:
                return HttpResponse("INVALID REQUEST!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return redirect("login_page")




def update_profile_view(request, *args, **kwargs):
    request_user = request.user
    request_user_id = request_user.pk

    #check if user is authenticated
    if request_user.is_authenticated:

        #check if parameter user is valid
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)
        if parameter_user:

            #check if parameter user is request user
            if parameter_user == request_user:
               
                if request.method == 'POST':
                    form = UpdateProfileForm(request.POST,request.FILES,instance=request_user_profile)
                    if form.is_valid():
                        form.save()
                        return redirect("user_profile_page", parameter_user_id=request_user_id)
                    else:
                        print("==========================================================")
                        print("INVALID FORM!")
                        print("==========================================================")
                        return redirect("update_profile_page", parameter_user_id=request_user_id)

                elif request.method == 'GET':
                    context = {}
                    request_user_profile = Profile.objects.get(user=request_user)
                    context['user_id'] = request_user_id
                    context['username'] = request_user.username
                    context['profile_image_src'] = request_user_profile.image.url
                    return render(request, "accounts/update_profile.html",context)
                else:
                    return HttpResponse("INVALID REQUEST!")
            else:
                return HttpResponse("DENIED ACCESS!")
        else:
            return HttpResponse("INVALID ID!")
    else:
        return HttpResponse("LOGIN REQUIRED!")
