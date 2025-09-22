from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    cantidad_disponible = models.IntegerField()
    imagen_url = models.URLField(max_length=200,default='https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)


class EstadoPedido(models.Model):
    estado = models.CharField(max_length=20)

class Pedido(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70)
    fecha_pedido = models.DateTimeField(auto_now_add=True) 
    estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE)  
    cantidad_producto = models.IntegerField(null=True, blank=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class MetodoPago(models.Model):
    metodo = models.CharField(max_length=100)    

class Venta(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)    

class EstadoEntrega(models.Model):
    estado = models.CharField(max_length=30)

class Entrega(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField()
    estado_entrega = models.ForeignKey(EstadoEntrega, on_delete=models.CASCADE)

class Contact(models.Model):
    motivo = models.CharField(max_length=100)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=100)
    respuesta = models.CharField(max_length=100,null=True, blank=True)

class HistorialPrecios(models.Model):
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha} - {self.precio}"
    