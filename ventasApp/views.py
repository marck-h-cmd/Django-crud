from django.shortcuts import render, redirect

from ventasApp.models import Categoria , Producto
from django.db.models import Q 
from .forms import CategoriaForm,ProductoForm
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
    categoria=Categoria.objects.get(idcategoria=id)
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
 categoria=Categoria.objects.get(idcategoria=id) 
 categoria.estado=False
 categoria.save()
 return redirect("listarcategoria") 


def listarproducto(request):
    queryset=request.GET.get("buscar")
    producto=Producto.objects.filter(estado=True) 
    if queryset:
        producto=Producto.objects.filter(Q(descripcion__icontains=queryset),estado=True).distinct() 
    context={'producto':producto}
    return render(request,"producto/listar.html",context) 

def agregarproducto(request):
    if request.method=="POST":
        form=ProductoForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("listarproducto") 
    else:
        form=ProductoForm()
    context={'form':form} 
    
    return render(request,"producto/agregar.html",context) 

def editarproducto(request,id):
    producto=Producto.objects.get(idproducto=id)
    if request.method=="POST":
        form=ProductoForm(request.POST,instance=producto)
        if form.is_valid():
            form.save() 
            return redirect("listarproducto") 
    else:
        form=ProductoForm(instance=producto)
    context={"form":form} 
    return render(request,"producto/editar.html",context) 

def eliminarproducto(request,id):
 producto=Producto.objects.get(idproducto=id) 
 producto.estado=False
 producto.save()
 return redirect("listarproducto") 