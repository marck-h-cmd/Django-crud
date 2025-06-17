from django.urls import path,include 
from ventasApp.views import listarcategoria,agregarcategoria,editarcategoria,eliminarcategoria
from django.contrib.auth import views

urlpatterns = [ 
               path('listacategoria/',listarcategoria,name="listarcategoria"),
               path('agregarcategoria/',agregarcategoria,name="agregarcategoria"),
               path('editarcategoria/<int:id>/',editarcategoria ,name="editarcategoria"),
               path('eliminarcategoria/<int:id>/',eliminarcategoria,name="eliminarcategoria"), 
               ] 