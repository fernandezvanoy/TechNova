from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from productos.models import Producto 
from django.contrib.auth.decorators import login_required

class Orden(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("enviado", "Enviado"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]

    id = models.AutoField(primary_key=True)
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ordenes"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        total = sum([item.subtotal for item in self.items.all()])
        self.total = total
        self.save()
        return total

    def __str__(self):
        return f"Orden {self.id} - {self.comprador}"

class ItemOrden(models.Model):
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey('pedidos.Orden', related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name="pago")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)
    codigo_transaccion = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - Orden {self.orden.id}"

class Envio(models.Model):
    ESTADOS_ENVIO = [
        ("pendiente", "Pendiente"),
        ("en camino", "En camino"),
        ("entregado", "Entregado"),
    ]

    id = models.AutoField(primary_key=True)
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name="envio")
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    metodo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS_ENVIO, default="pendiente")
    fecha_estimada = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Envío {self.id} - Orden {self.orden.id}"


class ConfirmacionVendedor(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="confirmaciones")
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("orden", "vendedor")
    
    def __str__(self):
        return f"Confirmación {self.vendedor} - Orden {self.orden.id}"