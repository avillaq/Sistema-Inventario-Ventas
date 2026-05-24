from decimal import Decimal

from django.core.management.base import BaseCommand

from inventory.models import Brand, Category, Product
from sales.models import Customer


class Command(BaseCommand):
    help = "Carga datos demo para probar inventario, POS y reportes."

    def handle(self, *args, **options):
        categories = {
            "Bebidas": Category.objects.get_or_create(name="Bebidas")[0],
            "Abarrotes": Category.objects.get_or_create(name="Abarrotes")[0],
            "Limpieza": Category.objects.get_or_create(name="Limpieza")[0],
        }
        brands = {
            "Andes": Brand.objects.get_or_create(name="Andes")[0],
            "Costa": Brand.objects.get_or_create(name="Costa")[0],
            "Hogar": Brand.objects.get_or_create(name="Hogar")[0],
        }

        products = [
            {
                "barcode": "775000100001",
                "name": "Agua mineral 625 ml",
                "cost": Decimal("0.90"),
                "price": Decimal("1.50"),
                "stock": 48,
                "min_stock": 12,
                "category": categories["Bebidas"],
                "brand": brands["Andes"],
            },
            {
                "barcode": "775000100002",
                "name": "Cafe molido 250 g",
                "cost": Decimal("8.20"),
                "price": Decimal("12.90"),
                "stock": 18,
                "min_stock": 6,
                "category": categories["Abarrotes"],
                "brand": brands["Costa"],
            },
            {
                "barcode": "775000100003",
                "name": "Detergente 900 g",
                "cost": Decimal("6.80"),
                "price": Decimal("10.50"),
                "stock": 5,
                "min_stock": 8,
                "category": categories["Limpieza"],
                "brand": brands["Hogar"],
            },
            {
                "barcode": "775000100004",
                "name": "Arroz extra 1 kg",
                "cost": Decimal("3.20"),
                "price": Decimal("4.80"),
                "stock": 35,
                "min_stock": 10,
                "category": categories["Abarrotes"],
                "brand": brands["Costa"],
            },
            {
                "barcode": "775000100005",
                "name": "Leche evaporada 400 g",
                "cost": Decimal("2.40"),
                "price": Decimal("3.70"),
                "stock": 42,
                "min_stock": 12,
                "category": categories["Abarrotes"],
                "brand": brands["Andes"],
            },
            {
                "barcode": "775000100006",
                "name": "Gaseosa cola 1.5 L",
                "cost": Decimal("4.10"),
                "price": Decimal("6.50"),
                "stock": 30,
                "min_stock": 10,
                "category": categories["Bebidas"],
                "brand": brands["Costa"],
            },
            {
                "barcode": "775000100007",
                "name": "Aceite vegetal 900 ml",
                "cost": Decimal("6.30"),
                "price": Decimal("9.20"),
                "stock": 22,
                "min_stock": 8,
                "category": categories["Abarrotes"],
                "brand": brands["Costa"],
            },
            {
                "barcode": "775000100008",
                "name": "Lavavajilla liquido 750 ml",
                "cost": Decimal("4.70"),
                "price": Decimal("7.40"),
                "stock": 16,
                "min_stock": 6,
                "category": categories["Limpieza"],
                "brand": brands["Hogar"],
            },
            {
                "barcode": "775000100009",
                "name": "Jugo de naranja 1 L",
                "cost": Decimal("3.10"),
                "price": Decimal("5.30"),
                "stock": 27,
                "min_stock": 9,
                "category": categories["Bebidas"],
                "brand": brands["Andes"],
            },
        ]

        customers = [
            {
                "full_name": "Ana Torres Quispe",
                "document_id": "45678912",
                "email": "ana.torres@example.com",
                "phone": "987654321",
                "is_active": True,
            },
            {
                "full_name": "Luis Ramirez Soto",
                "document_id": "56789123",
                "email": "luis.ramirez@example.com",
                "phone": "976543210",
                "is_active": True,
            },
            {
                "full_name": "Maria Flores Vega",
                "document_id": "67891234",
                "email": "maria.flores@example.com",
                "phone": "965432109",
                "is_active": True,
            },
            {
                "full_name": "Carlos Medina Rojas",
                "document_id": "78912345",
                "email": "carlos.medina@example.com",
                "phone": "954321098",
                "is_active": True,
            },
            {
                "full_name": "Rosa Castillo Leon",
                "document_id": "89123456",
                "email": "rosa.castillo@example.com",
                "phone": "943210987",
                "is_active": True,
            },
        ]

        created = 0
        updated = 0

        for data in products:
            _, was_created = Product.objects.update_or_create(
                barcode=data.pop("barcode"),
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        customers_created = 0
        customers_updated = 0
        for data in customers:
            _, was_created = Customer.objects.update_or_create(
                document_id=data.pop("document_id"),
                defaults=data,
            )
            if was_created:
                customers_created += 1
            else:
                customers_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Seed demo completado: "
                f"{created} productos creados, {updated} actualizados; "
                f"{customers_created} clientes creados, {customers_updated} actualizados."
            )
        )
