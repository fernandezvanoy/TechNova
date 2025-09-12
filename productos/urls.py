from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.producto_especifico, name="producto_especifico"),
    path("nuevo/", views.crear_producto, name="crear_producto"),
    path("<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path('<int:pk>/eliminar/', views.eliminar_producto1, name='eliminar_producto1'),
    path("mis-productos/", views.mis_productos, name="mis_productos"),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    
]


