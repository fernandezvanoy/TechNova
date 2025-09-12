from django import forms
from .models import Producto, CategoriaProducto, Reseña

# Formulario para crear o editar productos
class ProductoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=CategoriaProducto.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categorias']
        widgets = {
            # Estilos personalizados para los campos de texto
            'nombre': forms.TextInput(attrs={
                'class': 'px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'px-4 py-2 rounded-xl bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-white'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'text-white' 
            }),
        }

# Formulario para crear reseñas de productos
class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["calificacion", "comentario"]
        widgets = {
            "calificacion": forms.HiddenInput(),  # El valor se guarda oculto, no visible para el usuario
            "comentario": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Escribe tu opinión..."  # Mensaje guía para el usuario
            }),
        }
