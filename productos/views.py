from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Producto, CategoriaProducto
from pedidos.models import Orden, ItemOrden
from carrito.models import Carrito, ItemCarrito
from .forms import ProductoForm, ReseñaForm
from django.shortcuts import render
from django.db.models import Q
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




from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Producto, CategoriaProducto
from .forms import FiltroCategoriasForm

# RESULTADOS: solo busca por nombre y ahora acepta múltiples categorías por GET (?categorias=1&categorias=3)
def buscar_productos(request):
    q = (request.GET.get("q") or "").strip()
    categorias_ids = request.GET.getlist("categorias")  # múltiple
    qs = Producto.objects.select_related("vendedor").prefetch_related("categorias")

    if q:
        qs = qs.filter(nombre__icontains=q)

    if categorias_ids:
        for cid in categorias_ids:
            qs = qs.filter(categorias=cid)


    # orden por recientes
    qs = qs.order_by("-id")

    contexto = {
        "busqueda": q,
        "productos": qs,
        "categorias_seleccionadas": [int(x) for x in categorias_ids if x.isdigit()],
    }
    return render(request, "productos/buscar.html", contexto)


# Vista para los filtros de busqueda
def buscar_filtros(request):
    q = (request.GET.get("q") or "").strip()
    seleccion_inicial = request.GET.getlist("categorias")

    form = FiltroCategoriasForm(initial={
        "categorias": seleccion_inicial
    })

    if request.method == "POST":
        form = FiltroCategoriasForm(request.POST)
        if form.is_valid():
            categorias = form.cleaned_data.get("categorias") or []
            params = []
            if q:
                params.append(("q", q))
            for c in categorias:
                params.append(("categorias", str(c.id)))
            query = urlencode(params, doseq=True)
            return redirect(f"/buscar/?{query}" if query else "/buscar/")

    contexto = {
        "form": form,
        "busqueda": q,
        "categorias_actuales": seleccion_inicial,
    }
    return render(request, "productos/buscar_filtros.html", contexto)



# IMPLEMENTACIOPN API DE NOSOTROS
from rest_framework import viewsets
from .serializers import ProductoAdSerializer

class ProductoAdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.filter(stock__gt=0)
    serializer_class = ProductoAdSerializer


# API EXTERNA IMPLEMENTACION
# products/views.py
from django.shortcuts import render
import requests
import json

def obtener_productos_externos():
    """Obtiene productos de tecnología de API externa"""
    try:
        response = requests.get('https://fakestoreapi.com/products/category/electronics', timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def productos_externos(request):
    """Vista para productos externos usando template"""
    productos = obtener_productos_externos()
    productos = productos[:6] if productos else []
    
    # Convertir a JSON seguro para el template
    productos_json = json.dumps(productos) if productos else '[]'
    
    return render(request, 'productos/externos.html', {
        'productos_externos': productos,
        'productos_externos_json': productos_json  # Para el JavaScript
    })