from django.urls import path,include 
from ventasApp.views import (listarcategoria,agregarcategoria,editarcategoria,eliminarcategoria, 
                             listarproducto,agregarproducto,editarproducto,eliminarproducto,
                             listar_clientes, crear_cliente, actualizar_cliente, eliminar_cliente,crear_venta,listar_ventas)
from django.contrib.auth import views

urlpatterns = [ 
                path('listacategoria/',listarcategoria,name="listarcategoria"),
                path('agregarcategoria/',agregarcategoria,name="agregarcategoria"),
                path('editarcategoria/<int:id>/',editarcategoria ,name="editarcategoria"),
                path('eliminarcategoria/<int:id>/',eliminarcategoria,name="eliminarcategoria"), 
                
                path('listaproducto/',listarproducto,name="listarproducto"),
                path('agregarproducto/',agregarproducto,name="agregarproducto"),
                path('editarproducto/<int:id>/',editarproducto ,name="editarproducto"),
                path('eliminarproducto/<int:id>/',eliminarproducto,name="eliminarproducto"), 

                path('listarclientes/', listar_clientes, name="listar_clientes"),
                path('crearcliente/', crear_cliente, name="crear_cliente"),
                path('actualizarcliente/<int:id>/', actualizar_cliente, name="actualizar_cliente"),
                path('eliminarcliente/<int:id>/', eliminar_cliente, name="eliminar_cliente"),
                
                path('ventas/', listar_ventas, name='listar_ventas'),
                path('ventas/crear/', crear_venta, name='crear_venta'),

            ] 