


from django.contrib import admin
from django.urls import path
from seguridadApp.views import acceder,homePage,logout
urlpatterns = [
    path('',acceder,name="login"),
    path('home/',homePage,name="home"),
    path('logout/',logout,name="logout")

]
