from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RegisterUserForm, LoginUserForm



@api_view(['POST','GET'])
def create_user_view(request):
    user = request.user
    if user.is_authenticated:
        return Response({"ALREADY AUTHENTICATED!"},status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username').lower()
                raw_password = form.cleaned_data.get('password1')

                try:
                    account = authenticate(username=username, password=raw_password)
                    login(request, account)

                    print("==========================================================")
                    print(f"Name: {username}")
                    print(f"Password: {raw_password}")
                    print("==========================================================")
                    return redirect('home')
                except:

            else:
                return redirect('create_user')

        elif request.method == 'GET':
            return render(request, 'accounts/create_user.html')
        else:
            return Response({"message":"INVALID REQUEST!"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def login_user_view(request):
    user = request.user
    if user.is_authenticated:
        return Response({"message":"ALREADY AUTHENTICATED!"},status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("home")
        elif request.method == 'GET':
            return render(request, "accounts/login_user.html")
        else:
            return Response({"message":"INVALID REQUEST!"},status=status.HTTP_400_BAD_REQUEST)



def UserAccountLogoutView(request):
    logout(request)
    return redirect("home")


@api_view(['POST','GET'])
def update_user_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = UserAccount.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("Denied Access")
    context = {}
    if request.POST:
        form = UserAccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_account_profile", user_id=account.pk)
        else:
            context['form'] = form
    else:
        form = UserAccountUpdateForm(instance=request.user)
        context['form'] = form
    return render(request, "user_account/update_user_account.html", context)



