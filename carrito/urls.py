from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('eliminar/<int:item_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
]
