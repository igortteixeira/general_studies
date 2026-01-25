from django.urls import path
from django.contrib.auth import views as auth_views

import accounts.views as views



urlpatterns = [

#user
path("create_user/",views.create_user_view,name='create_user_api'),
path("user_profile/<int:user_id>",views.read_profile_user_view,name='user_profile_api'),


path("create_favourite/",views.create_favourite_view,name='create_favourite_api'),
path("delete_favourite/",views.delete_favourite_view,name='delete_favourite_api'),

path("user_favourite_list/<int:user_id>",views.list_favourite_user_view,name='user_favourite_list_api')
]
