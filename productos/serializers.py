from rest_framework import serializers
from .models import Producto

class ProductoAdSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "imagen_url", "detail_url"]

    def get_imagen_url(self, obj):
        request = self.context.get("request")
        if obj.imagen:
            return request.build_absolute_uri(obj.imagen.url)
        return None

    def get_detail_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/productos/{obj.id}/")
