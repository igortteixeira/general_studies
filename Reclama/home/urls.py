from django.urls import path
import home.views as views


urlpatterns = [
path("",views.home_view,name='home_page'),
path("searching/",views.searching_view,name='searching_page'),
path("user_favorite_list/",views.user_favorite_list_view,name='user_favorite_list_page'),
path("favorite/<int:parameter_object_type>/<int:parameter_object_id>/<str:parameter_path_name>",views.favorite_view,name='favorite_page'),
path("unfavorite/<int:parameter_favorite_id>/<str:parameter_path_name>",views.unfavorite_view,name='unfavorite_page'),
]
