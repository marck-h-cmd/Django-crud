from django.urls import path,include 
from ventasApp.views import (listarcategoria,agregarcategoria,editarcategoria,eliminarcategoria, 
                             listarproducto,agregarproducto,editarproducto,eliminarproducto,
                             listar_clientes, crear_cliente, actualizar_cliente, eliminar_cliente,crear_venta,listar_ventas,
                             producto_codigo,por_tipo,cliente_id,listarunidad,agregarunidad,editarunidad,eliminarunidad
                             ,cancelar_venta)
from django.contrib.auth import views

urlpatterns = [ 
                path('listacategoria/',listarcategoria,name="listarcategoria"),
                path('agregarcategoria/',agregarcategoria,name="agregarcategoria"),
                path('editarcategoria/<int:id>/',editarcategoria ,name="editarcategoria"),
                path('eliminarcategoria/<int:id>/',eliminarcategoria,name="eliminarcategoria"), 
                
                path('listaunidad/',listarunidad,name="listarunidad"),
                path('agregarunidad/',agregarunidad,name="agregarunidad"),
                path('editarunidad/<int:id>/',editarunidad ,name="editarunidad"),
                path('eliminarunidad/<int:id>/',eliminarunidad,name="eliminarunidad"), 
                
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
                path('ventas/cancelar/<int:id>/', cancelar_venta, name='cancelar_venta'),
                path('mostrarProducto/<int:idproducto>/', producto_codigo, name='producto_buscar'),
                path('mostrarTipo/<int:id>/', por_tipo, name='tipo_buscar'),
                path('mostrarCliente/<int:id>/',cliente_id,name='cliente_buscar')
            ] 