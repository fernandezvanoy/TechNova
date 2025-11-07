from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Producto
from decimal import Decimal

User = get_user_model()

class ApiProductosTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="vendedor1")
        Producto.objects.create(
            nombre="Laptop Pro 13",
            descripcion="Potente y ligera",
            precio=Decimal("4299000.00"),
            stock=5,
            vendedor=self.user,
        )

    def test_list_endpoint_ok(self):
        url = reverse("api_productos_list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("results", data)
        self.assertGreaterEqual(data["count"], 1)
        self.assertIn("nombre", data["results"][0])

    def test_detail_endpoint_ok(self):
        p = Producto.objects.first()
        url = reverse("api_productos_detail", args=[p.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], p.id)
        self.assertEqual(data["nombre"], p.nombre)
