from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Orden, Pago, Envio
from pedidos.models import ItemOrden, ConfirmacionVendedor
from django.db.models import Count
from django.utils import timezone

# i18n para mensajes cuando se usen (messages.success/info/error, etc.)
from django.utils.translation import gettext as _
from django.utils.translation import ngettext


@login_required
def orden_actual(request):
    orden = Orden.objects.filter(comprador=request.user, estado="pendiente").first()
    return render(request, "pedidos/orden_actual.html", {"orden": orden})


@login_required
def lista_ordenes(request):
    ordenes = Orden.objects.filter(comprador=request.user).order_by('-id')
    return render(request, "pedidos/lista.html", {"ordenes": ordenes})


@login_required
def detalle_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk, comprador=request.user)
    return render(request, "pedidos/detalle_orden.html", {"orden": orden})


@login_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk, comprador=request.user, estado='pendiente')
    orden.delete()
    # Si más adelante agregas messages, envuelve el texto: messages.success(request, _("Orden eliminada."))
    return redirect('lista_ordenes')


@login_required
def datos_envio(request, pk):
    orden = get_object_or_404(Orden, pk=pk, comprador=request.user)

    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        metodo = request.POST.get('metodo')

        envio, created = Envio.objects.get_or_create(orden=orden)
        envio.direccion = direccion
        envio.ciudad = ciudad
        envio.codigo_postal = codigo_postal
        envio.metodo = metodo
        envio.save()

        return redirect('pago', pk=orden.pk)

    return render(request, 'pedidos/datos_envio.html', {'orden': orden})


# Simulación de Pago
@login_required
def pago(request, pk):
    orden = get_object_or_404(Orden, pk=pk, comprador=request.user)

    if request.method == 'POST':
        metodo = request.POST.get('metodo')
        monto = orden.total

        Pago.objects.create(
            orden=orden,
            monto=monto,
            metodo=metodo,
            codigo_transaccion="SIMULADO123"  # Texto no visible; no requiere i18n
        )

        orden.estado = "pagada"  # Valor interno; no traducir
        orden.save()

        vendedores = {item.producto.vendedor for item in orden.items.all()}
        for v in vendedores:
            ConfirmacionVendedor.objects.get_or_create(orden=orden, vendedor=v)

        # Si agregas messages: messages.success(request, _("Pago registrado correctamente."))
        return redirect('lista_ordenes')

    return render(request, 'pedidos/pago.html', {'orden': orden})


@login_required
def ordenes_vendedor(request):
    ordenes = (
        ItemOrden.objects.filter(producto__vendedor=request.user)
        .values("orden__id", "orden__estado")
        .annotate(total_items=Count("id"))
    )
    return render(request, "pedidos/ordenes_vendedor.html", {"ordenes": ordenes})


@login_required
def detalle_orden_vendedor(request, pk):
    orden = get_object_or_404(Orden, pk=pk)

    items_vendedor = orden.items.filter(producto__vendedor=request.user)

    return render(
        request,
        "pedidos/detalle_orden_vendedor.html",
        {"orden": orden, "items": items_vendedor},
    )


@login_required
def confirmar_orden_vendedor(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    confirmacion = get_object_or_404(
        ConfirmacionVendedor, orden=orden, vendedor=request.user
    )
    confirmacion.confirmado = True
    confirmacion.fecha_confirmacion = timezone.now()
    confirmacion.save()

    # Cuando todos confirman, se marca como enviado (valor interno)
    if not orden.confirmaciones.filter(confirmado=False).exists():
        orden.estado = "enviado"
        orden.save()

    # Ejemplo futuro con messages: messages.success(request, _("Confirmación registrada."))
    return redirect("ordenes_vendedor")
