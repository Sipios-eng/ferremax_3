from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Producto)
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(MetodoPago)
admin.site.register(Venta)
admin.site.register(EstadoEntrega)
admin.site.register(Entrega)