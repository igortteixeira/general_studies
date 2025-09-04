from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from friendships.models import FriendRelation
from accounts.models import Profile
from .models import FriendsChat
from .forms import FriendsChatForm


def friend_chat_view(request, *args, **kwargs):
    request_user = request.user

    #check if user is logged
    if request_user.is_authenticated:
        parameter_user_id = kwargs.get("parameter_user_id")
        parameter_user = User.objects.get(pk=parameter_user_id)

        #check if both users are different
        if parameter_user and parameter_user!=request_user:

            #check if parameter user is friend
            request_parameter_users_relation = FriendRelation.objects.filter(self_user=request_user,friend_user=parameter_user)
            if  request_parameter_users_relation:

                if request.method == 'GET':

                    context = {}
                    parameter_user_profile = Profile.objects.get(user=parameter_user)

                    friends_chats = FriendsChat.objects.filter(sender=request_user,receiver=parameter_user) | FriendsChat.objects.filter(sender=parameter_user,receiver=request_user)
                    friends_chats_ordered = friends_chats.order_by('date_created')

                    context['messages'] = friends_chats_ordered
                    context['parameter_user_id'] = parameter_user_id
                    context['parameter_user_username'] = parameter_user.username
                    context['parameter_user_image_src'] = parameter_user_profile.image.url
                    return render(request, "chats/friend_chat.html",context)

                elif request.method == 'POST':

                    friends_chat_form = FriendsChatForm(request.POST)

                    #check if message is valid
                    if friends_chat_form.is_valid():
                        message_body = friends_chat_form.cleaned_data.get('body')

                        friends_chat_object = FriendsChat.objects.create(sender=request_user,receiver=parameter_user,body=message_body)
                        friends_chat_object.save()

                        print("==========================================================")
                        print("MESSAGE SENT SUCCESSFULLY!")
                        print("==========================================================")

                        return redirect("friend_chat_page", parameter_user_id=parameter_user_id)

                    else:
                        print("==========================================================")
                        print("INVALID FORM!")
                        print("==========================================================")
                        return redirect("friend_chat_page", parameter_user_id=parameter_user_id)
                else:
                    return HttpResponse("INVALID REQUEST!")
            else:
                return HttpResponse("PARAMETER USER IS NOT FRIEND!")
        else:
            return HttpResponse("INVALID USER!")
    else:
        return HttpResponse("LOGIN REQUIRED!")