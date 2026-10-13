import csv
from decimal import Decimal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Dealer, Product


class Command(BaseCommand):
    help = "Load catalogue.csv and dealers.csv from data/ into PostgreSQL. Safe to run repeatedly."

    def handle(self, *args, **options):
        data_dir = settings.DATA_DIR

        cat_path = data_dir / "catalogue.csv"
        dealers_path = data_dir / "dealers.csv"

        if not cat_path.exists():
            self.stdout.write(self.style.ERROR(f"Catalogue not found at {cat_path}"))
            return
        if not dealers_path.exists():
            self.stdout.write(self.style.ERROR(f"Dealers not found at {dealers_path}"))
            return

        with transaction.atomic():
            # Seed catalogue
            cat_count = 0
            with open(cat_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sku = row["sku"].strip()
                    price = Decimal(row["price"].strip())
                    stock = int(row["stock"].strip())
                    Product.objects.update_or_create(
                        sku=sku,
                        defaults={
                            "name": row["name"].strip(),
                            "category": row["category"].strip(),
                            "brand": row["brand"].strip(),
                            "vehicle_fitment": row["vehicle_fitment"].strip(),
                            "price": price,
                            "stock": stock,
                            "description": row["description"].strip(),
                        },
                    )
                    cat_count += 1

            # Seed dealers
            dealer_count = 0
            with open(dealers_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dealer_code = row["dealer_code"].strip()
                    credit_limit = Decimal(row["credit_limit"].strip())
                    Dealer.objects.update_or_create(
                        dealer_code=dealer_code,
                        defaults={
                            "name": row["name"].strip(),
                            "city": row.get("city", "").strip(),
                            "phone": row.get("phone", "").strip(),
                            "email": row.get("email", "").strip(),
                            "gstin": row.get("gstin", "").strip(),
                            "credit_limit": credit_limit,
                        },
                    )
                    dealer_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database: {cat_count} products ({Product.objects.count()} total), "
                f"{dealer_count} dealers ({Dealer.objects.count()} total)."
            )
        )
