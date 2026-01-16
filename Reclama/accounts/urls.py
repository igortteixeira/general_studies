from django.urls import path
from django.contrib.auth import views as auth_views

import accounts.views as views



urlpatterns = [

#user
path("create_user/",views.create_user_view,name='create_user_api')

]
