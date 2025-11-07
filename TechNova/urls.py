from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Ruta especial que Django usa para cambiar idioma 
    path("i18n/", include("django.conf.urls.i18n")),
]


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("productos.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("ordenes/", include("pedidos.urls")),
    path("carrito/", include("carrito.urls")),
    prefix_default_language=False,  
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
