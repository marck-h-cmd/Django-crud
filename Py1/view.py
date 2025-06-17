from django.http import HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render

class Persona(object):
    def __init__(self,nombre,apellido,edad):
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad

def saludo(request):
    p1=Persona("Juan","Diaz",14)            
    doc_externo=get_template('plantilla.html')
    documento=doc_externo.render({"nombre":p1.nombre,"apellido":p1.apellido,"edad":p1.edad})
    return HttpResponse(documento)

def acceder(request):
    return render(request,"login.html")
