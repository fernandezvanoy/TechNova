from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from productos.models import Producto
from pedidos.models import Orden, ItemOrden

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    carrito.calcular_total()
    return render(request, "carrito/carrito.html", {"carrito": carrito})

@login_required
def agregar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    cantidad = int(request.POST.get("cantidad", 1))

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": cantidad}
    )

    if not creado:
        item.cantidad += cantidad
        item.save()

    return redirect("ver_carrito")


@login_required
def eliminar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect("ver_carrito")

@login_required
def confirmar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.items.exists():
        return redirect("ver_carrito")

    orden = Orden.objects.create(comprador=request.user, estado="pendiente")

    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            subtotal=item.subtotal
        )


    orden.calcular_total()


    carrito.items.all().delete()

    return redirect("lista_ordenes")



