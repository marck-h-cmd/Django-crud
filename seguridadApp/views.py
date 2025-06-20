from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db.models import Count
from ventasApp.views import Categoria,Producto,Cliente
def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect("home") 
            else:
                messages.error(request,"Los datos son incorrectos") 

     
        return render(request, "login.html", {"form": form})
    else:
        messages.error(request,"Los datos son incorrectos") 
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})
    
def homePage(request):
    total_productos = Producto.objects.filter(estado=True).count()
    total_categorias = Categoria.objects.filter(estado=True).count()
    total_clientes = Cliente.objects.filter(estado=True).count()
    productos_sin_stock = Producto.objects.filter(stock=0, estado=True).count()
    
    
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_clientes': total_clientes,
        'productos_sin_stock': productos_sin_stock,
    }
    return render(request,"bienvenido.html",context) 


def salir(request):
    messages.info(request,"Saliste exitosamente") 
def logout(request):
    return redirect("login")