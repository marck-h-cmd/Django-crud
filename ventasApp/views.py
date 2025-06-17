from django.shortcuts import render, redirect

from ventasApp.models import Categoria 
from django.db.models import Q

from ventasApp.models import Categoria 
from django.db.models import Q 
from .forms import CategoriaForm
# Create your views here.
def listarcategoria(request):
    queryset=request.GET.get("buscar")
    categoria=Categoria.objects.filter(estado=True) 
    if queryset:
        categoria=Categoria.objects.filter(Q(descripcion__icontains=queryset),estado=True).distinct() 
        context={'categoria':categoria}
    return render(request,"categoria/listar.html",context) 
def agregarcategoria(request):
    if request.method=="POST":
        form=CategoriaForm(request.POST)
    if form.is_valid():
        form.save() 
        return redirect("listarcategoria") 
    else:
        form=CategoriaForm()
        context={'form':form} 
    return render(request,"categoria/agregar.html",context) 

def editarcategoria(request,id):
    categoria=Categoria.objects.get(id=id)
    if request.method=="POST":
        form=CategoriaForm(request.POST,instance=categoria)
    if form.is_valid():
        form.save() 
        return redirect("listarcategoria") 
    else:
        form=CategoriaForm(instance=categoria)
        context={"form":form} 
    return render(request,"categoria/editar.html",context) 

def eliminarcategoria(request,id):
 categoria=Categoria.objects.get(id=id) 
 categoria.estado=False
 categoria.save()
 return redirect("listarcategoria") 