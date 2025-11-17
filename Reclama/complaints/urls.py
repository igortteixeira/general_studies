from django.urls import path
from django.contrib.auth import views as auth_views

import complaints.views as views


urlpatterns = [
path("user_complaint_list/",views.user_complaint_list_view,name='user_complaint_list_page'),

#CRUD COMPLAINTS
path("create_complaint/<int:parameter_company_id>/",views.create_complaint_view,name='create_complaint_page'),
path("update_complaint/<int:parameter_complaint_id>/",views.update_complaint_view,name='update_complaint_page'),
path("delete_complaint/<int:parameter_complaint_id>/",views.delete_complaint_view,name='delete_complaint_page'),
path("read_complaint/<int:parameter_complaint_id>/",views.read_complaint_view,name='read_complaint_page'),
path("close_complaint/<int:parameter_complaint_id>/",views.close_complaint_view,name='close_complaint_page'),

#CRUD COMMENTS
path("create_comment/<int:parameter_complaint_id>/",views.create_comment_view,name='create_complaint_page'),
path("update_comment/<int:parameter_comment_id>/",views.update_comment_view,name='update_comment_page'),
]