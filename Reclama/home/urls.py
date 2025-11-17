from django.urls import path
import home.views as views


urlpatterns = [
path("",views.home_view,name='home_page'),
path("searching/",views.searching_view,name='searching_page'),
]

#path("favourite_companies/",views.favourite_companies_view,name='favourite_companies_page'),