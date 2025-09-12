from django.conf import settings
from django.db import models
from productos.models import Producto



class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrito'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        """
        Calcula el total del carrito sumando los subtotales de los items
        y lo guarda en el campo 'total'.
        """
        total = sum([item.subtotal for item in self.items.all()])
        self.total = total
        self.save()
        return total

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    id = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        """
        Retorna el subtotal de este item (precio * cantidad)
        """
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.username}"
