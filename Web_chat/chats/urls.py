from django.urls import path
import chats.views as views


urlpatterns = [
path("friend_chat/<int:parameter_user_id>/",views.friend_chat_view,name='friend_chat_page'),
]
