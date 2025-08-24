from django.urls import path
import friendships.views as views


urlpatterns = [
path("accept_friend_request/<int:parameter_user_id>/",views.accept_friend_request_view,name='accept_friend_request_page'),
path("reject_friend_request/<int:parameter_user_id>/",views.reject_friend_request_view,name='reject_friend_request_page'),
path("make_friend_request/<int:parameter_user_id>/",views.make_friend_request_view,name='make_friend_request_page'),
path("cancel_friend_request/<int:parameter_user_id>/",views.cancel_friend_request_view,name='cancel_friend_request_page'),
path("remove_friend/<int:parameter_user_id>/",views.remove_friend_view,name='remove_friend_page'),
]
