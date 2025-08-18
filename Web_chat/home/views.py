from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


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


def searching_view(request):
    if request.method == 'GET':
        try:
            parameter_search_string = kwargs.get("parameter_search_string")
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