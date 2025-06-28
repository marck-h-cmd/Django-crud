from django.shortcuts import render, redirect

from ventasApp.models import Categoria , Producto, Cliente,CabeceraVenta,DetalleVenta,Tipo,Parametro
from django.db.models import Q 
from django.contrib import messages
from .forms import CategoriaForm,ProductoForm, ClienteForm,CabeceraVentaForm
from django.http import JsonResponse
from django.core.paginator import Paginator
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
            messages.success(request, '¡Categoría creada exitosamente!') 
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
            messages.success(request, '¡Categoría actualizada exitosamente!')
            return redirect("listarcategoria") 
    else:
        form=CategoriaForm(instance=categoria)
    context={"form":form} 
    return render(request,"categoria/editar.html",context) 

def eliminarcategoria(request,id):
 categoria=Categoria.objects.get(idcategoria=id) 
 categoria.estado=False
 categoria.save()
 messages.success(request, '¡Categoría eliminada exitosamente!')
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
            messages.success(request, '¡Producto creado exitosamente!') 
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
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect("listarproducto") 
    else:
        form=ProductoForm(instance=producto)
    context={"form":form} 
    return render(request,"producto/editar.html",context) 

def eliminarproducto(request,id):
    producto=Producto.objects.get(idproducto=id) 
    producto.estado=False
    producto.save()
    messages.success(request, '¡Producto eliminado exitosamente!')
    return redirect("listarproducto") 

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente creado exitosamente!') 
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, id):
    cliente = Cliente.objects.get(idcliente=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente actualizado exitosamente!')
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/actualizar_cliente.html', {'form': form})

def eliminar_cliente(request, id):
    cliente = Cliente.objects.get(idcliente=id)
    if request.method == 'POST':
        cliente.estado = False
        cliente.save()
        messages.success(request, '¡Cliente eliminado exitosamente!')
        return redirect('listar_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})


def crear_venta(request):
    if request.method == 'POST':
        form = CabeceraVentaForm(request.POST)
        if form.is_valid():

            cabecera = form.save(commit=False)
            
            productos = request.POST.getlist('cod_producto[]')
            unidades = request.POST.getlist('unidad[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('pventa[]')

            subtotal = 0
            detalles = []
            
            for i in range(len(productos)):
                if productos[i] and cantidades[i] and precios[i]:
                    cantidad = float(cantidades[i])
                    precio = float(precios[i])
                    item_total = cantidad * precio
                    subtotal += item_total
                    
                    detalles.append({
                        'producto_id': productos[i],
                        'unidad': unidades[i],
                        'cantidad': cantidad,
                        'precio': precio,
                        'subtotal': item_total
                    })
            
            cabecera.subtotal = subtotal
            cabecera.igv = subtotal * 0.18  
            cabecera.total = subtotal * 1.18
            cabecera.save()
            

            for detalle in detalles:
                DetalleVenta.objects.create(
                    venta=cabecera,
                    idproducto=detalle['producto_id'],
                    precio=detalle['precio'],
                    cantidad=detalle['cantidad']
                )
            
            messages.success(request, 'Venta registrada con éxito!')
            return redirect('listar_ventas')
    else:
        form = CabeceraVentaForm()
    
    tipos = Tipo.objects.all()
    productos = Producto.objects.filter(estado=True)
    

    tipo_default = tipos.first()
    parametros = Parametro.objects.filter(tipo=tipo_default).first()
    
    context = {
        'form': form,
        'tipos': tipos,
        'productos': productos,
        'nrodoc_default': parametros.numeracion if parametros else ''
    }
    return render(request, 'ventas/agregar.html', context)

def listar_ventas(request):
    buscarpor = request.GET.get('buscarpor', '')
    
    if buscarpor:
        ventas = CabeceraVenta.objects.filter(
            Q(nrodoc__icontains=buscarpor) |
            Q(cliente__nomcliente__icontains=buscarpor) |
            Q(cliente__ruc_dni__icontains=buscarpor)
        ).select_related('tipo', 'cliente').order_by('-fecha_venta')
    else:
        ventas = CabeceraVenta.objects.all().select_related('tipo', 'cliente').order_by('-fecha_venta')
    
   
    paginator = Paginator(ventas, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'buscarpor': buscarpor,
    }
    return render(request, 'ventas/listar.html', context)