from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from productos.models import Producto


class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.DecimalField(
        _("Total"),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carrito",
        verbose_name=_("Usuario")
    )
    fecha_creacion = models.DateTimeField(
        _("Fecha de creación"),
        auto_now_add=True
    )

    def calcular_total(self):
        """
        {% trans "Calcula el total del carrito sumando los subtotales de los items
        y lo guarda en el campo 'total'." %}
        """
        total = sum([item.subtotal for item in self.items.all()])
        self.total = total
        self.save()
        return total

    def __str__(self):
        # Traducción dinámica
        return _("Carrito de %(usuario)s") % {"usuario": self.usuario.username}

    class Meta:
        verbose_name = _("Carrito")
        verbose_name_plural = _("Carritos")


class ItemCarrito(models.Model):
    id = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(
        Carrito,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_("Carrito")
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        verbose_name=_("Producto")
    )
    cantidad = models.PositiveIntegerField(
        _("Cantidad"),
        default=1
    )

    @property
    def subtotal(self):
        """
        {% trans "Retorna el subtotal de este ítem (precio * cantidad)" %}
        """
        return self.cantidad * self.producto.precio

    def __str__(self):
        return _("%(cantidad)s x %(producto)s en el carrito de %(usuario)s") % {
            "cantidad": self.cantidad,
            "producto": self.producto.nombre,
            "usuario": self.carrito.usuario.username
        }

    class Meta:
        verbose_name = _("Ítem de carrito")
        verbose_name_plural = _("Ítems de carrito")
