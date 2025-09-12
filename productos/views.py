from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Producto, CategoriaProducto
from pedidos.models import Orden, ItemOrden
from carrito.models import Carrito, ItemCarrito
from .forms import ProductoForm, ReseñaForm
import random


# Vista de inicio, muestra todos los productos y selecciona uno destacado aleatoriamente
def home(request):
    productos = Producto.objects.all()
    destacado = None
    if productos.exists():
        destacado = random.choice(productos)

    return render(request, "productos/home.html", {
        "productos": productos,
        "destacado": destacado
    })


# Vista de un producto específico, permite ver el detalle, agregar al carrito o crear reseñas
def producto_especifico(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    reseñas = producto.reseñas.all().order_by("-fecha")

    if request.method == "POST":
        # Agregar producto al carrito
        if "cantidad" in request.POST:
            if not request.user.is_authenticated:
                return redirect("login")

            cantidad = int(request.POST.get("cantidad", 1))
            carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

            item, creado = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={"cantidad": cantidad}
            )
            if not creado:
                item.cantidad += cantidad
                item.save()

            return redirect("ver_carrito")

        # Crear una reseña para el producto
        else:
            if not request.user.is_authenticated:
                return redirect("login")

            form = ReseñaForm(request.POST)
            if form.is_valid():
                reseña = form.save(commit=False)
                reseña.producto = producto
                reseña.usuario = request.user
                reseña.save()
                return redirect("producto_especifico", pk=pk)
    else:
        form = ReseñaForm()

    return render(request, "productos/producto_especifico.html", {
        "producto": producto,
        "reseñas": reseñas,
        "form": form,
    })


# Vista para crear un producto nuevo
@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user  # Asigna el usuario actual como vendedor
            producto.save()
            return redirect("home")
    else:
        form = ProductoForm()
    return render(request, "productos/crear_producto.html", {"form": form})


# Vista para editar un producto existente
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if producto.vendedor != request.user:
        raise PermissionDenied  # Evita que otros usuarios editen este producto

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("producto_especifico", pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(request, "productos/editar_producto.html", {"form": form, "producto": producto})


# Vista para eliminar un producto
@login_required
def eliminar_producto1(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if producto.vendedor != request.user:
        raise PermissionDenied  # Solo el vendedor puede eliminar su producto

    if request.method == "POST":
        producto.delete()
        return redirect("home")

    return render(request, "productos/eliminar_producto.html", {"producto": producto})


# Vista que muestra todos los productos del usuario
@login_required
def mis_productos(request):
    productos = Producto.objects.filter(vendedor=request.user)
    return render(request, "productos/mis_productos.html", {"productos": productos})


# Vista para buscar productos por nombre
def buscar_productos(request):
    query = request.GET.get('q')  # Toma el texto de búsqueda
    productos = []
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Filtra productos que contengan la búsqueda

    return render(request, 'productos/buscar.html', {
        'productos': productos,
        'busqueda': query
    })
