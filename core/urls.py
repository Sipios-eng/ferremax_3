from django.urls import path
from .views import *

urlpatterns = [

    path('',index, name="index"),
    path('auth_register/',auth_register,name='auth_register'),
    path('auth_login/',auth_login,name='auth_login'),
    path('logout/',exit,name='exit'),
    path('stock_products/',stock_products,name='stock'),
    path('pedidos/',pedidos,name='pedidos'),
    path('pedido_aceptado/<int:pedido_id>/',aceptar_pedido,name='aceptar_pedido'),
    path('pedido_eliminado/<int:pedido_id>/',eliminar_pedido,name='eliminar_pedido'),
    path('solicitud_bodega/',solicitud_bodega,name='solicitudes'),
    path('cart/',cart,name='cart'),
    path('cart/add/',agregar_producto,name='agregar'),
    path('cart/update/',update_producto,name='updateCart'),
    path('cart/delete/',delete_producto,name='deleteCart'),
    path('productos/',productos,name='productos'),
    path('entrega/',entrega,name='entrega'),
    path('edit_entrega/<int:id_entrega>/',edit_entrega,name='edit_entrega'),
    path('producto/<int:producto_id>/', verProducto, name='verProducto'),
    path('contact/',contact, name='contact'),
    path('success_pay/',success_pay,name='successPay'),
    path('consultas_clientes',consulta_cliente,name='consultaCliente'),
    path('mis_consultas/<int:user_id>',mis_consultas,name='mis_consultas'),
    path('getApi/',obtener_datos_api,name='getApi'),
    path('registrar_entrega/',registrar_entrega, name='registrarEntrega'),
    path('agregar_producto/',add_product, name='agregar_producto'),
    path('eliminar_producto/',delete_product, name='eliminar_producto'),
    path('eliminar_producto/<int:producto_id>',borrar_producto,name='borrar_producto'),
    path('eliminar_multiples_productos/', borrar_multiples_productos,name='borrar_multiples_productos'),
    path('buscar/',buscar_productos,name='busqueda'),
    path('eliminar_categorias',eliminar_categorias,name='eliminar_categorias'),
    path('actualizar_producto/',actualizar_producto,name='actualizar_producto'),
    path('editar_producto/<int:id_producto>/',edit_producto,name='edit_producto'),
    path('historialPrecios/<int:id_producto>/',historialPrecios,name='historialPrecios'),
    path('historialPrecios/<int:id_producto>/exportarPdf/',exportarPdf,name='exportarPdf')
]