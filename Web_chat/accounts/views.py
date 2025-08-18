from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, UpdateProfileForm#,LoginUserForm
from .models import Profile



def create_user_view(request):
    request_user = request.user
    if request_user.is_authenticated:
        return HttpResponse("LOGOUT REQUIRED!")
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = UpdateProfileForm(request.POST,request.FILES)

            #fix
            if form.is_valid() and profile_form.is_valid():
                user_instance = form.save()
                profile_image = profile_form.cleaned_data.get('image')
                profile_instance = Profile.objects.create(user=user_instance,image=profile_image)
                profile_instance.save()

                try:
                    username = form.cleaned_data.get('username').lower()
                    raw_password = form.cleaned_data.get('password1')
                    account = authenticate(username=username, password=raw_password)
                    login(request, account)

                    print("==========================================================")
                    print("USER CREATED AND LOGGED!")
                    print(f"Username: {username}, Password:{raw_password}")
                    print("==========================================================")
                    return redirect('home_page')
                except:
                    print("==========================================================")
                    print("LOGIN ERROR!")
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

'''
def login_user_view(request):
    request_user = request.user
    if request_user.is_authenticated:
        return HttpResponse("LOGOUT REQUIRED!")
    else:
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data.get('username').lower()
                    raw_password = form.cleaned_data.get('password')
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
    if not request_user.is_authenticated:
        return HttpResponse("LOGIN REQUIRED!")
    else:
        if request.method == 'POST':
            try:
                logout(request)
                print("==========================================================")
                print("LOGGED OUT!")
                print("==========================================================")
                return redirect("home_page")
            except:
                print("==========================================================")
                print("LOGOUT ERROR!")
                print("==========================================================")
                return redirect('logout_page')

        elif request.method == 'GET':
            context = {}
            context['username'] = request_user.username
            return render(request, "accounts/logout.html",context)
        else:
            return HttpResponse("INVALID REQUEST!")


def user_profile_view(request, *args, **kwargs):
    if request.method == 'GET':
        context = {}
        is_self = False
        parameter_user_id = kwargs.get("parameter_user_id")
        request_user = request.user
        request_user_id = request_user.pk
        try:
            parameter_user = User.objects.get(pk=parameter_user_id)
            parameter_user_profile = Profile.objects.get(user=parameter_user)
        except:
            return HttpResponse("INVALID ID!")
        
        if request_user == parameter_user:
            is_self = True
            request_user_profile = Profile.objects.get(user=request_user)
            context['user_id'] = request_user_id
            context['username'] = request_user.username
            context['profile_image_src'] = request_user_profile.image.url
            context['is_self'] = is_self
        else:
            context['user_id'] = parameter_user_id
            context['username'] = parameter_user.username
            context['profile_image_src'] = parameter_user_profile.image.url
            context['is_self'] = is_self

        return render(request, "accounts/user_profile.html",context)
    else:
        return HttpResponse("INVALID REQUEST!")


def update_profile_view(request, *args, **kwargs):
    request_user = request.user
    if not request_user.is_authenticated:
        return HttpResponse("LOGIN REQUIRED!")
    else:

        parameter_user_id = kwargs.get("parameter_user_id")
        request_user_id = request_user.pk
        request_user_profile = Profile.objects.get(user=request_user)
        try:
            parameter_user = User.objects.get(pk=parameter_user_id)
        except:
            return HttpResponse("INVALID ID!")

        if parameter_user != request_user:
           return HttpResponse("Denied Access!")
        else:
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
                context['user_id'] = request_user_id
                context['username'] = request_user.username
                context['profile_image_src'] = request_user_profile.image.url
                return render(request, "accounts/update_profile.html",context)
            else:
                return HttpResponse("INVALID REQUEST!")