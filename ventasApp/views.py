from django.shortcuts import render, redirect

from ventasApp.models import Categoria , Producto, Cliente,CabeceraVenta,DetalleVenta,Tipo,Parametro
from django.db.models import Q, F
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
    print("POST keys:", request.POST.keys())  # Para ver todas las claves

    print("cod_producto:", request.POST.getlist('cod_producto'))
    print("unidad:", request.POST.getlist('unidad'))
    print("cantidad:", request.POST.getlist('cantidad'))
    print("pventa:", request.POST.getlist('pventa'))
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
            print("ERRORES EN FORMULARIO:", form.errors)
    else:
        form = CabeceraVentaForm()
    
    tipos = Tipo.objects.all()
    clientes = Cliente.objects.filter(estado=True)
    productos = Producto.objects.filter(estado=True)
    

    tipo_default = tipos.first()
    parametros = Parametro.objects.filter(tipo=tipo_default).first()
    
    context = {
        'form': form,
        'tipos': tipos,
        'clientes': clientes,
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
        ).select_related('tipo', 'cliente').order_by('fecha_venta')
    else:
        ventas = CabeceraVenta.objects.all().select_related('tipo', 'cliente').order_by('fecha_venta')
    
   
    paginator = Paginator(ventas, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'buscarpor': buscarpor,
    }
    return render(request, 'ventas/listar.html', context)

def producto_codigo(request, idproducto):
    try:
        producto = (Producto.objects
                    .filter(estado=1, idproducto=idproducto)
                    .select_related('idunidad')
                    .annotate(unidad=F('idunidad__descripcion'))
                    .values(
                        'idproducto',
                        'descripcion',
                        'unidad',
                        'precio',
                        'stock'
                    )
                    .first())

        if producto is None:
            return JsonResponse({'error': f'No se encontró el producto con ID {idproducto}'}, status=404)

        # Forzar conversión de Decimal a float
        if 'precio' in producto:
            producto['precio'] = float(producto['precio'])

        return JsonResponse(producto)
    except Exception as e:
        print("ERROR EN producto_codigo:", e)  # 👈 Añade esta línea
        return JsonResponse({'error': str(e)}, status=500)

    
def por_tipo(request, id):
    try:
        datos_qs = (Parametro.objects
                    .filter(tipo_id=id)
                    .annotate(descripcion_tipo=F('tipo__descripcion'))
                    .values('serie', 'numeracion', 'descripcion_tipo'))
        datos_list = list(datos_qs)

        if not datos_list:
            return JsonResponse(
                {'error': f'No se encontraron datos para el tipo con ID {id}'},
                status=404
            )

        return JsonResponse(datos_list, safe=False)

    except Exception as e:
        # Imprimimos el error real en consola para depurar
        print("ERROR en por_tipo:", repr(e))
        return JsonResponse({'error': str(e)}, status=500)
    
def cliente_id(request, id):
    try:
        c = Cliente.objects.get(pk=id)
        return JsonResponse({'ruc_dni': c.ruc_dni, 'direccion': c.direccion})
    except Cliente.DoesNotExist:
        return JsonResponse({}, status=404)