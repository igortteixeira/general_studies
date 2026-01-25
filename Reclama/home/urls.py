from django.urls import path
import home.views as views


urlpatterns = [
path("search/",views.list_search_view,name='search_page')
]
