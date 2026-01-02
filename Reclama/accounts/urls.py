from django.urls import path
from django.contrib.auth import views as auth_views

import accounts.views as views



urlpatterns = [
path("users_list/",views.users_list_view,name='users_list_page'),

#user
path("choose_user_type/",views.choose_user_type_view,name='choose_user_type_page'),
path("create_user/<int:user_type_choice>/",views.create_user_view,name='create_user_page'),

#Profile managment
path("user_profile/<int:parameter_user_id>/",views.user_profile_view,name='user_profile_page'),
path("update_profile/",views.update_profile_view,name='update_profile_page'),

#favorites
path("user_favorite_list/",views.user_favorite_list_view,name='user_favorite_list_page'),
path("favorite/<int:parameter_object_type>/<int:parameter_object_id>/<str:parameter_path_name>",views.favorite_view,name='favorite_page'),
path("unfavorite/<int:parameter_favorite_id>/<str:parameter_path_name>",views.unfavorite_view,name='unfavorite_page'),

#Authentication
path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login_page'),
path("logout/",views.logout_user_view,name='logout_page'),

#Password Change
path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),name='password_change'),
path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]
