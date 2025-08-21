from django.urls import path
import home.views as views


urlpatterns = [
path("",views.home_view,name='home_page'),
path("search_users/",views.search_users_view,name='search_users_page'),
#path("search_users/<str:parameter_search_string>",views.search_users_view,name='search_users_page'),
]