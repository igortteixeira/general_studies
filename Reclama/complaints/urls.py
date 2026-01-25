from django.urls import path
from django.contrib.auth import views as auth_views

import complaints.views as views


urlpatterns = [
#CRUD COMPLAINTS
path("create_complaint/<int:user_id>/<int:company_id>",views.create_complaint_view,name='create_complaint_api'),
path("read_complaint/<int:user_id>/<int:complaint_id>",views.read_complaint_view,name='read_complaint_api'),
path("update_complaint/<int:user_id>/<int:complaint_id>",views.update_complaint_view,name='update_complaint_api'),
path("close_complaint/<int:parameter_complaint_id>/",views.close_complaint_view,name='close_complaint_api'),

path("user_complaint_list/<int:user_id>",views.list_complaint_user_view,name='user_complaint_list_api'),
path("complaints_list/",views.list_complaint_view,name='complaints_list_api'),


#CRUD COMMENTS
path("create_comment/<int:user_id>/<int:complaint_id>",views.create_comment_view,name='create_comment_api')
]