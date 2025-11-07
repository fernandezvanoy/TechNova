from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Producto, CategoriaProducto, Reseña


# Formulario para crear o editar productos
class ProductoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=CategoriaProducto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_("Categorías"),
        help_text=_("Selecciona una o varias categorías para el producto"),
    )

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "imagen", "categorias"]
        labels = {
            "nombre": _("Nombre"),
            "descripcion": _("Descripción"),
            "precio": _("Precio"),
            "stock": _("Cantidad disponible"),
            "imagen": _("Imagen"),
        }
        help_texts = {
            "precio": _("Ingresa el precio con dos decimales"),
            "stock": _("Número de unidades disponibles"),
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white",
                "placeholder": _("Nombre del producto"),
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white",
                "placeholder": _("Descripción del producto"),
            }),
            "precio": forms.NumberInput(attrs={
                "class": "px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white",
                "placeholder": _("Precio"),
            }),
            "stock": forms.NumberInput(attrs={
                "class": "px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white",
                "placeholder": _("Cantidad en stock"),
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "text-white",
            }),
        }


# Formulario para crear reseñas de productos
class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["calificacion", "comentario"]
        labels = {
            "calificacion": _("Calificación"),
            "comentario": _("Comentario"),
        }
        widgets = {
            "calificacion": forms.HiddenInput(),
            "comentario": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": _("Escribe tu opinión..."),
            }),
        }


# Formulario para filtrar productos por categorías
class FiltroCategoriasForm(forms.Form):
    categorias = forms.ModelMultipleChoiceField(
        label=_("Categorías"),
        queryset=CategoriaProducto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text=_("Selecciona una o varias categorías para filtrar los productos"),
    )
