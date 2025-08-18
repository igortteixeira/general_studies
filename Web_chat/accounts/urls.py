from django.urls import path
from django.contrib.auth import views as auth_views

import accounts.views as views


urlpatterns = [
path("create_user/",views.create_user_view,name='create_user_page'),
path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login_page'),
#path("login/",views.login_user_view,name='login_page'),
path("logout/",views.logout_user_view,name='logout_page'),
path("user_profile/<int:parameter_user_id>/",views.user_profile_view,name='user_profile_page'),
path("update_profile/<int:parameter_user_id>/",views.update_profile_view,name='update_profile_page'),

#Password Change
path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),name='password_change'),
path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]