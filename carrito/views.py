from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Carrito, ItemCarrito
from productos.models import Producto
from pedidos.models import Orden, ItemOrden

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.calcular_total()
    return render(request, "carrito/carrito.html", {"carrito": carrito})

@login_required
def agregar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    cantidad = int(request.POST.get("cantidad", 1))

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": cantidad},
    )
    if not creado:
        item.cantidad += cantidad
        item.save()

    messages.success(
        request,
        _("“%(nombre)s” fue agregado al carrito (x%(cantidad)s).") % {
            "nombre": producto.nombre,
            "cantidad": cantidad,
        },
    )
    return redirect("ver_carrito")

@login_required
def eliminar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    nombre = item.producto.nombre
    item.delete()
    messages.info(request, _("Se eliminó “%(nombre)s” del carrito.") % {"nombre": nombre})
    return redirect("ver_carrito")

@login_required
def confirmar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.items.exists():
        messages.warning(request, _("Tu carrito está vacío."))
        return redirect("ver_carrito")

    orden = Orden.objects.create(comprador=request.user, estado="pendiente")

    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            subtotal=item.subtotal,
        )

    orden.calcular_total()
    carrito.items.all().delete()

    messages.success(
        request,
        _("¡Compra confirmada! Tu pedido #%(id)s fue creado correctamente.") % {"id": orden.id},
    )
    return redirect("lista_ordenes")
