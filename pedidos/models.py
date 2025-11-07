from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from productos.models import Producto
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


class Orden(models.Model):
    ESTADOS = [
        ("pendiente", _("Pendiente")),
        ("pagada", _("Pagada")),
        ("enviado", _("Enviado")),
        ("completada", _("Completada")),
        ("cancelada", _("Cancelada")),
    ]

    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ordenes",
        verbose_name=_("Comprador"),
        help_text=_("Usuario que realiza la compra."),
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación"),
        help_text=_("Fecha y hora en que se creó la orden."),
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
        verbose_name=_("Estado"),
        help_text=_("Estado actual de la orden."),
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Total"),
        help_text=_("Valor total de la orden."),
    )

    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Órdenes")

    def calcular_total(self):
        total = sum([item.subtotal for item in self.items.all()])
        self.total = total
        self.save()
        return total

    def __str__(self):
        return f"Orden {self.id} - {self.comprador}"


class ItemOrden(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    orden = models.ForeignKey(
        "pedidos.Orden",
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_("Orden"),
        help_text=_("Orden a la que pertenece este ítem."),
    )
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        verbose_name=_("Producto"),
        help_text=_("Producto asociado al ítem."),
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Cantidad"),
        help_text=_("Cantidad del producto en la orden."),
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Subtotal"),
        help_text=_("Subtotal del ítem (precio × cantidad)."),
    )

    class Meta:
        verbose_name = _("Ítem de orden")
        verbose_name_plural = _("Ítems de orden")

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)


class Pago(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    orden = models.OneToOneField(
        Orden,
        on_delete=models.CASCADE,
        related_name="pago",
        verbose_name=_("Orden"),
        help_text=_("Orden asociada al pago."),
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Monto"),
        help_text=_("Monto pagado por la orden."),
    )
    metodo = models.CharField(
        max_length=50,
        verbose_name=_("Método de pago"),
        help_text=_("Método utilizado para realizar el pago."),
    )
    codigo_transaccion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Código de transacción"),
        help_text=_("Identificador de la transacción (si aplica)."),
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de pago"),
        help_text=_("Fecha y hora en que se registró el pago."),
    )

    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")

    def __str__(self):
        return f"Pago {self.id} - Orden {self.orden.id}"


class Envio(models.Model):
    ESTADOS_ENVIO = [
        ("pendiente", _("Pendiente")),
        ("en camino", _("En camino")),
        ("entregado", _("Entregado")),
    ]

    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    orden = models.OneToOneField(
        Orden,
        on_delete=models.CASCADE,
        related_name="envio",
        verbose_name=_("Orden"),
        help_text=_("Orden asociada al envío."),
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name=_("Dirección"),
        help_text=_("Dirección de entrega."),
    )
    ciudad = models.CharField(
        max_length=100,
        verbose_name=_("Ciudad"),
        help_text=_("Ciudad de entrega."),
    )
    codigo_postal = models.CharField(
        max_length=20,
        verbose_name=_("Código postal"),
        help_text=_("Código postal de la dirección."),
    )
    metodo = models.CharField(
        max_length=50,
        verbose_name=_("Método de envío"),
        help_text=_("Método de envío seleccionado."),
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_ENVIO,
        default="pendiente",
        verbose_name=_("Estado del envío"),
        help_text=_("Estado actual del envío."),
    )
    fecha_estimada = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Fecha estimada de entrega"),
        help_text=_("Fecha estimada para la entrega (si aplica)."),
    )

    class Meta:
        verbose_name = _("Envío")
        verbose_name_plural = _("Envíos")

    def __str__(self):
        return f"Envío {self.id} - Orden {self.orden.id}"


class ConfirmacionVendedor(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name="confirmaciones",
        verbose_name=_("Orden"),
        help_text=_("Orden que requiere confirmación del vendedor."),
    )
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Vendedor"),
        help_text=_("Vendedor que confirma el envío."),
    )
    confirmado = models.BooleanField(
        default=False,
        verbose_name=_("Confirmado"),
        help_text=_("Indica si el vendedor ya confirmó."),
    )
    fecha_confirmacion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Fecha de confirmación"),
        help_text=_("Fecha y hora de la confirmación (si aplica)."),
    )

    class Meta:
        unique_together = ("orden", "vendedor")
        verbose_name = _("Confirmación de vendedor")
        verbose_name_plural = _("Confirmaciones de vendedores")

    def __str__(self):
        return f"Confirmación {self.vendedor} - Orden {self.orden.id}"
