from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductoAdViewSet

router = DefaultRouter()
router.register(r"api/anuncios", ProductoAdViewSet, basename="anuncios")

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.producto_especifico, name="producto_especifico"),
    path("nuevo/", views.crear_producto, name="crear_producto"),
    path("<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("<int:pk>/eliminar/", views.eliminar_producto1, name="eliminar_producto1"),
    path("mis-productos/", views.mis_productos, name="mis_productos"),

    # BUSQUEDA
    path("buscar/", views.buscar_productos, name="buscar_productos"),
    path("buscar/filtros/", views.buscar_filtros, name="buscar_filtros"),

    # API NUESTRA
    path("", include(router.urls)),

    # API EXTERNA
    path('productos-externos/', views.productos_externos, name='productos_externos'),
]
