from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils.translation import ngettext


def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Ejemplo futuro con mensajes:
            # messages.success(request, _("Tu cuenta ha sido creada exitosamente."))
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "usuarios/registro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Ejemplo: messages.success(request, _("Has iniciado sesión correctamente."))
            return redirect("home")
        # Ejemplo: messages.error(request, _("Nombre de usuario o contraseña incorrectos."))
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


def logout_view(request):
    logout(request)
    # Ejemplo: messages.info(request, _("Has cerrado sesión correctamente."))
    return redirect("login")
