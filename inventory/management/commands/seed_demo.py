from decimal import Decimal

from django.core.management.base import BaseCommand

from inventory.models import Brand, Category, Product


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

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed demo completado: {created} productos creados, {updated} actualizados."
            )
        )
