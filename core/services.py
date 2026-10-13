import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.utils import timezone
import pytz

from core.models import (
    Product,
    Dealer,
    Order,
    OrderItem,
    OrderDailySequence,
    InventoryLog,
)
from core.exceptions import CustomAPIException

KOLKATA_TZ = pytz.timezone("Asia/Kolkata")


def generate_order_number() -> str:
    """Generate unique ORD-YYYYMMDD-NNNN using Asia/Kolkata and atomic sequence in DB."""
    now_ist = timezone.now().astimezone(KOLKATA_TZ)
    date_str = now_ist.strftime("%Y%m%d")

    with transaction.atomic():
        seq_obj, _ = OrderDailySequence.objects.select_for_update().get_or_create(
            date_str=date_str, defaults={"last_seq": 0}
        )
        seq_obj.last_seq += 1
        seq_obj.save()
        return f"ORD-{date_str}-{seq_obj.last_seq:04d}"


def hash_request_body(body_data) -> str:
    serialized = json.dumps(body_data, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def calculate_order_totals(items_data):
    """
    items_data: list of dicts with {'sku', 'quantity'} or existing OrderItem objects
    Returns: (computed_items, subtotal, tax_total, grand_total)
    """
    tax_rate = Decimal("0.18")
    subtotal = Decimal("0.00")
    tax_total = Decimal("0.00")
    computed_items = []

    for item in items_data:
        sku = item["sku"]
        quantity = int(item["quantity"])
        product = item["product"]
        unit_price = product.price

        line_subtotal = (unit_price * quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        line_tax = (line_subtotal * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        line_total = line_subtotal + line_tax

        subtotal += line_subtotal
        tax_total += line_tax

        computed_items.append(
            {
                "product": product,
                "sku": sku,
                "name": product.name,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_subtotal": line_subtotal,
                "line_tax": line_tax,
                "line_total": line_total,
            }
        )

    grand_total = subtotal + tax_total
    return computed_items, subtotal, tax_total, grand_total


def validate_order_payload(dealer_id, items_raw):
    if not dealer_id:
        raise CustomAPIException(
            code="VALIDATION_ERROR",
            message="dealer_id is required",
            details=["dealer_id is required"],
            status_code=400,
        )

    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        raise CustomAPIException(
            code="VALIDATION_ERROR",
            message=f"Dealer with id {dealer_id} does not exist",
            details=[f"dealer_id {dealer_id} not found"],
            status_code=400,
        )

    if not isinstance(items_raw, list) or len(items_raw) == 0:
        raise CustomAPIException(
            code="VALIDATION_ERROR",
            message="items must be a non-empty list",
            details=["items must contain at least 1 item"],
            status_code=400,
        )

    seen_skus = set()
    sku_list = []
    for idx, it in enumerate(items_raw):
        if not isinstance(it, dict):
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message=f"Item at index {idx} must be an object",
                details=[f"Invalid item format at index {idx}"],
                status_code=400,
            )
        sku = it.get("sku")
        if not sku or not isinstance(sku, str):
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message=f"Item at index {idx} is missing a valid sku",
                details=[f"Missing sku at index {idx}"],
                status_code=400,
            )
        sku = sku.strip()
        if sku in seen_skus:
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message=f"Duplicate SKU '{sku}' found in items",
                details=[f"SKU {sku} cannot appear multiple times in the same order"],
                status_code=400,
            )
        seen_skus.add(sku)

        qty = it.get("quantity")
        if qty is None or not isinstance(qty, int) or qty < 1:
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message=f"Quantity for SKU '{sku}' must be an integer >= 1",
                details=[f"Invalid quantity {qty} for SKU {sku}"],
                status_code=400,
            )
        sku_list.append(sku)

    # Fetch products
    products = {p.sku: p for p in Product.objects.filter(sku__in=sku_list)}
    for sku in sku_list:
        if sku not in products:
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message=f"Product with SKU '{sku}' does not exist",
                details=[f"Unknown SKU: {sku}"],
                status_code=400,
            )

    prepared_items = []
    for it in items_raw:
        sku = it["sku"].strip()
        prepared_items.append(
            {
                "sku": sku,
                "quantity": it["quantity"],
                "product": products[sku],
            }
        )

    return dealer, prepared_items


def create_draft_order(dealer_id, items_raw, idempotency_key=None, raw_body=None) -> Order:
    body_hash = hash_request_body(raw_body) if raw_body is not None else None

    if idempotency_key:
        existing = Order.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            if existing.request_hash == body_hash:
                return existing
            else:
                raise CustomAPIException(
                    code="IDEMPOTENCY_CONFLICT",
                    message="Idempotency key has already been used with a different request body",
                    details=[f"Idempotency-Key {idempotency_key} conflict"],
                    status_code=409,
                )

    dealer, prepared_items = validate_order_payload(dealer_id, items_raw)

    with transaction.atomic():
        order_number = generate_order_number()
        computed_items, subtotal, tax_total, grand_total = calculate_order_totals(prepared_items)

        order = Order.objects.create(
            order_number=order_number,
            dealer=dealer,
            status="DRAFT",
            subtotal=subtotal,
            tax_total=tax_total,
            grand_total=grand_total,
            idempotency_key=idempotency_key,
            request_hash=body_hash,
        )

        order_items = [
            OrderItem(
                order=order,
                product=ci["product"],
                sku=ci["sku"],
                name=ci["name"],
                quantity=ci["quantity"],
                unit_price=ci["unit_price"],
                line_subtotal=ci["line_subtotal"],
                line_tax=ci["line_tax"],
                line_total=ci["line_total"],
            )
            for ci in computed_items
        ]
        OrderItem.objects.bulk_create(order_items)

    return order


def update_draft_order(order: Order, items_raw) -> Order:
    if order.status != "DRAFT":
        raise CustomAPIException(
            code="ORDER_LOCKED",
            message=f"Cannot edit order with status {order.status}",
            details=[f"Order {order.order_number} is locked because its status is {order.status}"],
            status_code=409,
        )

    _, prepared_items = validate_order_payload(order.dealer_id, items_raw)

    with transaction.atomic():
        computed_items, subtotal, tax_total, grand_total = calculate_order_totals(prepared_items)

        order.items.all().delete()

        order.subtotal = subtotal
        order.tax_total = tax_total
        order.grand_total = grand_total
        order.save()

        order_items = [
            OrderItem(
                order=order,
                product=ci["product"],
                sku=ci["sku"],
                name=ci["name"],
                quantity=ci["quantity"],
                unit_price=ci["unit_price"],
                line_subtotal=ci["line_subtotal"],
                line_tax=ci["line_tax"],
                line_total=ci["line_total"],
            )
            for ci in computed_items
        ]
        OrderItem.objects.bulk_create(order_items)

    return order


def confirm_order(order: Order) -> Order:
    if order.status != "DRAFT":
        raise CustomAPIException(
            code="INVALID_TRANSITION",
            message=f"Cannot confirm order from status {order.status}",
            details=[f"Allowed transition to CONFIRMED is only from DRAFT, got {order.status}"],
            status_code=409,
        )

    with transaction.atomic():
        # Lock products and order items
        items = list(order.items.select_related("product").all())
        sku_list = [it.sku for it in items]
        locked_products = {
            p.sku: p
            for p in Product.objects.select_for_update().filter(sku__in=sku_list)
        }

        short_lines = []
        messages = []
        for it in items:
            p = locked_products.get(it.sku)
            if not p or p.stock < it.quantity:
                avail = p.stock if p else 0
                short_lines.append(
                    {"sku": it.sku, "requested": it.quantity, "available": avail}
                )
                p_name = p.name if p else it.name
                messages.append(
                    f"Insufficient stock for {p_name}. Available: {avail}, Requested: {it.quantity}"
                )

        if short_lines:
            raise CustomAPIException(
                code="INSUFFICIENT_STOCK",
                message=" ".join(messages),
                details=short_lines,
                status_code=409,
            )

        # Deduct stock
        for it in items:
            p = locked_products[it.sku]
            p.stock -= it.quantity
            p.save(update_fields=["stock", "updated_at"])

        order.status = "CONFIRMED"
        order.save(update_fields=["status", "updated_at"])

    return order


def cancel_order(order: Order) -> Order:
    if order.status not in ["DRAFT", "CONFIRMED"]:
        raise CustomAPIException(
            code="INVALID_TRANSITION",
            message=f"Cannot cancel order from status {order.status}",
            details=[f"Allowed cancel status is DRAFT or CONFIRMED, got {order.status}"],
            status_code=409,
        )

    with transaction.atomic():
        if order.status == "CONFIRMED":
            items = list(order.items.select_related("product").all())
            sku_list = [it.sku for it in items]
            locked_products = {
                p.sku: p
                for p in Product.objects.select_for_update().filter(sku__in=sku_list)
            }
            for it in items:
                p = locked_products.get(it.sku)
                if p:
                    p.stock += it.quantity
                    p.save(update_fields=["stock", "updated_at"])

        order.status = "CANCELLED"
        order.save(update_fields=["status", "updated_at"])

    return order


def dispatch_order(order: Order) -> Order:
    if order.status != "CONFIRMED":
        raise CustomAPIException(
            code="INVALID_TRANSITION",
            message=f"Cannot dispatch order from status {order.status}",
            details=[f"Allowed dispatch status is CONFIRMED, got {order.status}"],
            status_code=409,
        )
    order.status = "DISPATCHED"
    order.save(update_fields=["status", "updated_at"])
    return order


def deliver_order(order: Order) -> Order:
    if order.status != "DISPATCHED":
        raise CustomAPIException(
            code="INVALID_TRANSITION",
            message=f"Cannot deliver order from status {order.status}",
            details=[f"Allowed deliver status is DISPATCHED, got {order.status}"],
            status_code=409,
        )
    order.status = "DELIVERED"
    order.save(update_fields=["status", "updated_at"])
    return order
