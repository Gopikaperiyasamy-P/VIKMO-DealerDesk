from decimal import Decimal
import os
import csv
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Product, Dealer, Order, OrderItem
from core.services import create_draft_order, confirm_order, cancel_order
from core.assistant import execute_search_parts, execute_check_stock, execute_create_draft_order, handle_chat
from core.forecast_service import load_forecast_metadata, get_sku_forecast, get_reorder_suggestions


class CoreBackendTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dealer = Dealer.objects.create(
            dealer_code="DLR-TEST-01",
            name="Apex Motors",
            credit_limit=Decimal("50000.00")
        )
        self.p1 = Product.objects.create(
            sku="BRK-1044",
            name="Brake Pad Set - Bajaj Pulsar 150",
            category="Brakes",
            brand="Endurance",
            vehicle_fitment="Bajaj Pulsar 150",
            price=Decimal("1459.50"),
            stock=100,
            description="Endurance brake pad set for Pulsar 150."
        )
        self.p2 = Product.objects.create(
            sku="OIL-1001",
            name="Coolant 1L - Universal",
            category="Engine & Oils",
            brand="Motul",
            vehicle_fitment="Universal",
            price=Decimal("604.25"),
            stock=50,
            description="Motul coolant."
        )

    def test_products_list_and_filter(self):
        r = self.client.get("/api/products/?search=Pulsar")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["count"], 1)
        self.assertEqual(r.json()["results"][0]["sku"], "BRK-1044")

        # Category filter
        r_cat = self.client.get("/api/products/?category=Brakes")
        self.assertEqual(r_cat.status_code, status.HTTP_200_OK)
        self.assertEqual(r_cat.json()["count"], 1)

    def test_product_post_and_duplicate_error(self):
        # Create valid
        r = self.client.post("/api/products/", {
            "sku": "NEW-001",
            "name": "New Part",
            "category": "Brakes",
            "brand": "Bosch",
            "vehicle_fitment": "Universal",
            "price": "999.00",
            "description": "Test"
        })
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json()["stock"], 0)

        # Duplicate SKU -> 409 DUPLICATE
        r_dup = self.client.post("/api/products/", {
            "sku": "NEW-001",
            "name": "Duplicate Part",
            "price": "500.00"
        })
        self.assertEqual(r_dup.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r_dup.json()["error"]["code"], "DUPLICATE")

    def test_inventory_update(self):
        r = self.client.put("/api/inventory/BRK-1044/", {"quantity": 75, "reason": "audit"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, 75)

    def test_order_creation_pricing_and_gst(self):
        r = self.client.post("/api/orders/", {
            "dealer_id": self.dealer.id,
            "items": [{"sku": "BRK-1044", "quantity": 2}]
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        b = r.json()
        self.assertEqual(b["status"], "DRAFT")
        # 1459.50 * 2 = 2919.00 subtotal
        # tax = 2919.00 * 0.18 = 525.42
        # total = 3444.42
        self.assertEqual(b["subtotal"], "2919.00")
        self.assertEqual(b["tax_total"], "525.42")
        self.assertEqual(b["grand_total"], "3444.42")

    def test_order_confirm_and_stock_deduction(self):
        order = create_draft_order(self.dealer.id, [{"sku": "BRK-1044", "quantity": 10}])
        confirmed = confirm_order(order)
        self.assertEqual(confirmed.status, "CONFIRMED")
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, 90)

        # Cancel restores stock
        cancelled = cancel_order(confirmed)
        self.assertEqual(cancelled.status, "CANCELLED")
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.stock, 100)


class AssistantAndForecastTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dealer = Dealer.objects.create(dealer_code="DLR-001", name="ABC Motors")
        self.product = Product.objects.create(
            sku="BRK-1044",
            name="Brake Pad Set - Bajaj Pulsar 150",
            category="Brakes",
            brand="Endurance",
            vehicle_fitment="Bajaj Pulsar 150",
            price=Decimal("1459.50"),
            stock=136
        )

    def test_assistant_tools_execution(self):
        # 1. search_parts
        res = execute_search_parts(query="brake pad", vehicle="Pulsar 150")
        self.assertTrue(len(res) > 0)
        self.assertEqual(res[0]["sku"], "BRK-1044")

        # 2. check_stock
        stk = execute_check_stock(["BRK-1044"])
        self.assertEqual(len(stk), 1)
        self.assertEqual(stk[0]["stock"], 136)

        # 3. create_draft_order
        summary, action = execute_create_draft_order(self.dealer.id, [{"sku": "BRK-1044", "quantity": 3}])
        self.assertEqual(action["type"], "draft_order_created")
        self.assertEqual(summary["status"], "DRAFT")

    def test_assistant_chat_api(self):
        r = self.client.post("/api/assistant/chat/", {
            "session_id": "test-sess-123",
            "dealer_id": self.dealer.id,
            "message": "Do you have brake pads for a Pulsar 150?"
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        b = r.json()
        self.assertIn("reply", b)
        self.assertIn("cited_skus", b)
        self.assertIn("tool_calls", b)
        self.assertIn("actions", b)
        self.assertIn("BRK-1044", b["cited_skus"])

    def test_forecast_file_structure(self):
        forecast_path = os.path.join("ml", "forecast.csv")
        self.assertTrue(os.path.exists(forecast_path))
        with open(forecast_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 160)
        weeks = {"2026-09-28", "2026-10-05", "2026-10-12", "2026-10-19"}
        found_weeks = {r["week_start"] for r in rows}
        self.assertEqual(weeks, found_weeks)
        for r in rows:
            self.assertGreaterEqual(float(r["forecast_units"]), 0.0)

    def test_forecast_and_reorder_apis(self):
        # Valid forecast SKU
        r = self.client.get("/api/forecast/FIL-1016/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        b = r.json()
        self.assertEqual(len(b["forecast"]), 4)

        # Non-forecast SKU -> 404
        r_invalid = self.client.get("/api/forecast/BRK-1044/")
        self.assertEqual(r_invalid.status_code, status.HTTP_404_NOT_FOUND)

        r2 = self.client.get("/api/reorder-suggestions/")
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        results = r2.json()["results"]
        self.assertEqual(len(results), 40)
        first = results[0]
        for k in ("sku", "current_stock", "lead_time_weeks", "lead_time_demand", "safety_stock", "reorder_point", "reorder_qty"):
            self.assertIn(k, first)
