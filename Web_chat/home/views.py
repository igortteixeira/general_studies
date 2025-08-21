from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from accounts.models import Profile



def home_view(request):
    if request.method == 'GET':
        context = {}
        is_authenticated = False
        request_user = request.user
        request_user_id = request_user.pk

        if request_user.is_authenticated:
            is_authenticated = True
            context['is_authenticated'] = is_authenticated
            context['user_id'] = request_user_id
        else:
            context['is_authenticated'] = is_authenticated

        return render(request,'home/home.html',context)
    else:
        return HttpResponse("INVALID REQUEST!")


def search_users_view(request, *args, **kwargs):
    if request.method == 'GET':
        context = {}
        list_users = []
        empty_result = True
        parameter_search_string = request.GET.get("parameter_search_string")

        if parameter_search_string:
            parameter_search_string_users = User.objects.filter(username__icontains=parameter_search_string)
            if parameter_search_string_users:
                empty_result = False

                for parameter_search_string_user in parameter_search_string_users:
                    parameter_search_string_user_profile = Profile.objects.get(user=parameter_search_string_user)

                    list_users.append({'id':parameter_search_string_user.pk,'username':parameter_search_string_user.username,'image_url':parameter_search_string_user_profile.image.url})

                context['empty_result'] = empty_result
                context['list_users'] = list_users
                return render(request,'home/search_users.html',context)

            else:
                context['empty_result'] = empty_result
                context['list_users'] = list_users
                return render(request,'home/search_users.html',context)
        else:
            context['empty_result'] = empty_result
            context['list_users'] = list_users
            return render(request,'home/search_users.html',context)
    else:
        return HttpResponse("INVALID REQUEST!")