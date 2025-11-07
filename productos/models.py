from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoriaProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(_("Nombre de la categoría"), max_length=100)
    descripcion = models.TextField(_("Descripción"), blank=True, null=True)

    class Meta:
        verbose_name = _("Categoría de producto")
        verbose_name_plural = _("Categorías de producto")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(_("Nombre del producto"), max_length=200)
    descripcion = models.TextField(_("Descripción"), blank=True)
    precio = models.DecimalField(_("Precio"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Cantidad disponible"), default=0)
    imagen = models.ImageField(_("Imagen"), upload_to="productos/", blank=True, null=True)

    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="productos",
        null=True,
        blank=True,
        verbose_name=_("Vendedor"),
    )

    categorias = models.ManyToManyField(
        CategoriaProducto,
        related_name="productos",
        blank=True,
        verbose_name=_("Categorías"),
    )

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")

    def __str__(self):
        return self.nombre


class Reseña(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        related_name="reseñas",
        on_delete=models.CASCADE,
        verbose_name=_("Producto"),
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Usuario"),
    )
    calificacion = models.PositiveSmallIntegerField(_("Calificación"))  # 1 a 5
    comentario = models.TextField(_("Comentario"), blank=True, null=True)
    fecha = models.DateTimeField(_("Fecha de publicación"), auto_now_add=True)

    class Meta:
        verbose_name = _("Reseña")
        verbose_name_plural = _("Reseñas")

    def __str__(self):
        return _("Reseña de %(usuario)s sobre %(producto)s") % {
            "usuario": self.usuario.username,
            "producto": self.producto.nombre,
        }
