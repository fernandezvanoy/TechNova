from django.conf import settings
from django.db import models



class CategoriaProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='productos',
        null=True, blank=True
    )

    categorias = models.ManyToManyField(
        CategoriaProducto,
        related_name='productos',
        blank=True
    )

    def __str__(self):
        return self.nombre


class Reseña(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, related_name='reseñas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calificacion = models.PositiveSmallIntegerField()  # 1 a 5
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario.username} sobre {self.producto.nombre}"


