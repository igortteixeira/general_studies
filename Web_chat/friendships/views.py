from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import FriendRelation,FriendRequest
from accounts.models import Profile


def accept_friend_request_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is NOT already friend
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            if not request_parameter_users_relation:

                #check if parameter user made an active friend request to request user
                parameter_user_friend_request = FriendRequest.objects.filter(requesting_user=parameter_user,requested_user=request_user)
                if parameter_user_friend_request:

                    if request.method == 'GET':

                        context = {}
                        parameter_user_profile = Profile.objects.get(user=parameter_user)

                        context['parameter_user_id'] = parameter_user_id
                        context['parameter_user_username'] = parameter_user.username
                        context['parameter_user_image_src'] = parameter_user_profile.image.url
                        return render(request, "friendships/accept_friend_request.html",context)

                    elif request.method == 'POST':
                        request_parameter_users_relation_object = FriendRelation.objects.create(self_user=request_user,friend_user=parameter_user)
                        parameter_request_users_relation_object = FriendRelation.objects.create(self_user=parameter_user,friend_user=request_user)

                        request_parameter_users_relation_object.save()
                        parameter_request_users_relation_object.save()
                        parameter_user_friend_request.delete()

                        print("==========================================================")
                        print("FRIEND REQUEST ACCEPTED!")
                        print("==========================================================")

                        return redirect("user_profile_page", parameter_user_id=parameter_user_id)

                    else:
                        return HttpResponse("INVALID REQUEST!")
                else:
                    return HttpResponse("PARAMETER USER MADE NO FRIEND REQUEST TO REQUEST USER")
            else:
                return HttpResponse("PARAMETER USER IS ALREADY FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")



def reject_friend_request_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)
        
        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is NOT already friend
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            if not request_parameter_users_relation:

                #check if parameter user made an active friend request to request user
                parameter_user_friend_request = FriendRequest.objects.filter(requesting_user=parameter_user,requested_user=request_user)
                if parameter_user_friend_request:

                    if request.method == 'GET':

                        context = {}
                        parameter_user_profile = Profile.objects.get(user=parameter_user)

                        context['parameter_user_id'] = parameter_user_id
                        context['parameter_user_username'] = parameter_user.username
                        context['parameter_user_image_src'] = parameter_user_profile.image.url
                        return render(request, "friendships/reject_friend_request.html",context)

                    elif request.method == 'POST':

                        parameter_user_friend_request.delete()
                        print("==========================================================")
                        print("FRIEND REQUEST REJECTED!")
                        print("==========================================================")

                        return redirect("user_profile_page", parameter_user_id=parameter_user_id)
                    else:
                        return HttpResponse("INVALID REQUEST!")
                else:
                    return HttpResponse("PARAMETER USER MADE NO FRIEND REQUEST TO REQUEST USER!")
            else:
                return HttpResponse("PARAMETER USER IS ALREADY FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")


def make_friend_request_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is NOT already friend
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            if not request_parameter_users_relation:

                #check if one of the users has NOT already made a friend request
                parameter_user_friend_request = FriendRequest.objects.filter(requesting_user=parameter_user,requested_user=request_user)
                request_user_friend_request = FriendRequest.objects.filter(requesting_user=request_user,requested_user=parameter_user)
                if not parameter_user_friend_request and not request_user_friend_request:

                    if request.method == 'GET':

                        context = {}
                        parameter_user_profile = Profile.objects.get(user=parameter_user)

                        context['parameter_user_id'] = parameter_user_id
                        context['parameter_user_username'] = parameter_user.username
                        context['parameter_user_image_src'] = parameter_user_profile.image.url
                        return render(request, "friendships/make_friend_request.html",context)

                    elif request.method == 'POST':

                        request_user_friend_request_object = FriendRequest.objects.create(requesting_user=request_user,requested_user=parameter_user)
                        request_user_friend_request_object.save()

                        print("==========================================================")
                        print("FRIEND REQUEST MADE!")
                        print("==========================================================")

                        return redirect("user_profile_page", parameter_user_id=parameter_user_id)
                    else:
                        return HttpResponse("INVALID REQUEST!")
                else:
                    return HttpResponse("FRIEND REQUEST ALREADY EXISTS!")
            else:
                return HttpResponse("PARAMETER USER IS ALREADY FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")



def cancel_friend_request_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is NOT already friend
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            if not request_parameter_users_relation:

                #check if request user made a friend request to parameter user
                request_user_friend_request = FriendRequest.objects.filter(requesting_user=request_user,requested_user=parameter_user)
                if request_user_friend_request:

                    if request.method == 'GET':

                        context = {}
                        parameter_user_profile = Profile.objects.get(user=parameter_user)

                        context['parameter_user_id'] = parameter_user_id
                        context['parameter_user_username'] = parameter_user.username
                        context['parameter_user_image_src'] = parameter_user_profile.image.url
                        return render(request, "friendships/cancel_friend_request.html",context)

                    elif request.method == 'POST':

                        request_user_friend_request.delete()
                        print("==========================================================")
                        print("FRIEND REQUEST CANCELLED!")
                        print("==========================================================")

                        return redirect("user_profile_page", parameter_user_id=parameter_user_id)
                    else:
                        return HttpResponse("INVALID REQUEST!")
                else:
                    return HttpResponse("NO FRIEND REQUEST MADE TO PARAMETER USER!")
            else:
                return HttpResponse("PARAMETER USER IS ALREADY FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")




def remove_friend_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is friend(perhaps the "and" is unecessary because...)
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            parameter_request_users_relation = FriendRelation.objects.filter(self_user=parameter_user,friend_user=request_user)
            if request_parameter_users_relation and parameter_request_users_relation:

                if request.method == 'GET':

                    context = {}
                    parameter_user_profile = Profile.objects.get(user=parameter_user)

                    context['parameter_user_id'] = parameter_user_id
                    context['parameter_user_username'] = parameter_user.username
                    context['parameter_user_image_src'] = parameter_user_profile.image.url
                    return render(request, "friendships/remove_friend.html",context)

                elif request.method == 'POST':

                    request_parameter_users_relation.delete()
                    parameter_request_users_relation.delete()
                    print("==========================================================")
                    print("FRIEND REQUEST CANCELLED!")
                    print("==========================================================")

                    return redirect("user_profile_page", parameter_user_id=parameter_user_id)
                else:
                    return HttpResponse("INVALID REQUEST!")
            else:
                return HttpResponse("PARAMETER USER IS ALREADY FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")
