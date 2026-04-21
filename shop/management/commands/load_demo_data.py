from django.core.management.base import BaseCommand
from django.db import transaction

from shop.data import CATEGORIES, PRODUCTS
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Загружает демонстрационные категории и товары в базу данных."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Loading categories...")
        by_slug: dict[str, Category] = {}
        for c in CATEGORIES:
            obj, _ = Category.objects.update_or_create(
                slug=c["slug"],
                defaults={"name": c["name"], "desc": c.get("desc", "")},
            )
            by_slug[obj.slug] = obj

        self.stdout.write("Loading products...")
        for p in PRODUCTS:
            cat = by_slug[p["category"]]
            Product.objects.update_or_create(
                id=p["id"],
                defaults={
                    "category": cat,
                    "name": p["name"],
                    "short": p.get("short", ""),
                    "price": p["price"],
                    "image_key": p.get("image", ""),
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
