from django.urls import path
from . import views

urlpatterns = [
    path("mis-ordenes/", views.lista_ordenes, name="lista_ordenes"),
    path("orden/<int:pk>/", views.detalle_orden, name="detalle_orden"),
    path("orden/<int:pk>/eliminar/", views.eliminar_orden, name="eliminar_orden"),
    path("orden/<int:pk>/envio/", views.datos_envio, name="datos_envio"),
    path("orden/<int:pk>/pago/", views.pago, name="pago"),

    # 🔹 Para los vendedores
    path("mis-ordenes-vendedor/", views.ordenes_vendedor, name="ordenes_vendedor"),
    path("orden-vendedor/<int:pk>/", views.detalle_orden_vendedor, name="detalle_orden_vendedor"),
    path("orden-vendedor/<int:pk>/confirmar/", views.confirmar_orden_vendedor, name="confirmar_orden_vendedor"),
]
