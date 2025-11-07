from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.utils.translation import gettext_lazy as _


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'password1', 'password2']
        labels = {
            'username': _("Nombre de usuario"),
            'email': _("Correo electrónico"),
            'rol': _("Rol"),
            'password1': _("Contraseña"),
            'password2': _("Confirmar contraseña"),
        }
        help_texts = {
            'username': _("Escribe tu nombre de usuario."),
            'email': _("Ingresa tu correo electrónico válido."),
            'rol': _("Selecciona el rol correspondiente."),
            'password1': _("Tu contraseña debe tener al menos 8 caracteres."),
            'password2': _("Repite la contraseña para confirmar."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadimos placeholders traducibles
        self.fields['username'].widget.attrs.update({
            'placeholder': _("Tu nombre de usuario")
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': _("Tu correo electrónico")
        })
        self.fields['rol'].widget.attrs.update({
            'placeholder': _("Selecciona tu rol")
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': _("Tu contraseña")
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': _("Confirma tu contraseña")
        })
