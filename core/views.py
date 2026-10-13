from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import CustomAPIException
from core.models import Dealer, InventoryLog, Order, Product
from core.pagination import StandardResultsSetPagination
from core.serializers import (
    DealerCreateSerializer,
    DealerSerializer,
    OrderSerializer,
    ProductCreateSerializer,
    ProductSerializer,
)
from core.services import (
    cancel_order,
    confirm_order,
    create_draft_order,
    deliver_order,
    dispatch_order,
    update_draft_order,
)


def health(request):
    """GET /api/health/ — the grader polls this until your app is ready."""
    return JsonResponse({"status": "ok"})


class ProductListView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        qs = Product.objects.all()

        search = request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(sku__icontains=search)
                | Q(name__icontains=search)
                | Q(brand__icontains=search)
            )

        category = request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)

        vehicle = request.query_params.get("vehicle")
        if vehicle:
            qs = qs.filter(vehicle_fitment__icontains=vehicle)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        sku = data.get("sku")
        if not sku or not isinstance(sku, str) or not sku.strip():
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="sku is required",
                details=["sku is required"],
                status_code=400,
            )
        sku = sku.strip()
        if Product.objects.filter(sku=sku).exists():
            raise CustomAPIException(
                code="DUPLICATE",
                message=f"Product with SKU '{sku}' already exists",
                details=[f"SKU {sku} already exists"],
                status_code=409,
            )

        serializer = ProductCreateSerializer(data=data)
        if not serializer.is_valid():
            errors = []
            for field, err_list in serializer.errors.items():
                for e in err_list:
                    errors.append(f"{field}: {e}")
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="Validation error: " + (errors[0] if errors else "Invalid product data"),
                details=errors,
                status_code=400,
            )

        validated = serializer.validated_data
        product = Product.objects.create(
            sku=validated["sku"].strip(),
            name=validated["name"].strip(),
            category=validated.get("category", "").strip(),
            brand=validated.get("brand", "").strip(),
            vehicle_fitment=validated.get("vehicle_fitment", "").strip(),
            price=validated["price"],
            stock=0,
            description=validated.get("description", "").strip(),
        )
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get_object(self, sku):
        try:
            return Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Product with SKU '{sku}' not found",
                details=[f"Product '{sku}' does not exist"],
                status_code=404,
            )

    def get(self, request, sku):
        product = self.get_object(sku)
        return Response(ProductSerializer(product).data)

    def patch(self, request, sku):
        product = self.get_object(sku)
        data = request.data

        if "sku" in data and data["sku"] != sku:
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="SKU cannot be changed",
                details=["Product SKU is immutable"],
                status_code=400,
            )

        if "price" in data:
            try:
                price_val = Decimal(str(data["price"]))
                if price_val <= Decimal("0.00") or price_val.as_tuple().exponent < -2:
                    raise ValueError()
                product.price = price_val
            except Exception:
                raise CustomAPIException(
                    code="VALIDATION_ERROR",
                    message="Price must be a positive number with at most 2 decimal places",
                    details=["Invalid price value"],
                    status_code=400,
                )

        for field in ["name", "category", "brand", "vehicle_fitment", "description"]:
            if field in data:
                setattr(product, field, str(data[field]))

        product.save()
        return Response(ProductSerializer(product).data)


class InventoryUpdateView(APIView):
    def put(self, request, sku):
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Product with SKU '{sku}' not found",
                details=[f"Product '{sku}' does not exist"],
                status_code=404,
            )

        qty = request.data.get("quantity")
        if qty is None or not isinstance(qty, int) or qty < 0:
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="quantity must be an integer >= 0",
                details=["Invalid quantity; must be integer >= 0"],
                status_code=400,
            )

        reason = request.data.get("reason", "")
        product.stock = qty
        product.save(update_fields=["stock", "updated_at"])

        InventoryLog.objects.create(product=product, quantity=qty, reason=str(reason))

        return Response({"sku": product.sku, "quantity": product.stock})


class DealerListView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        qs = Dealer.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = DealerSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        dealer_code = data.get("dealer_code")
        if not dealer_code or not isinstance(dealer_code, str) or not dealer_code.strip():
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="dealer_code is required",
                details=["dealer_code is required"],
                status_code=400,
            )
        dealer_code = dealer_code.strip()
        if Dealer.objects.filter(dealer_code=dealer_code).exists():
            raise CustomAPIException(
                code="DUPLICATE",
                message=f"Dealer with code '{dealer_code}' already exists",
                details=[f"Dealer code {dealer_code} already exists"],
                status_code=409,
            )

        serializer = DealerCreateSerializer(data=data)
        if not serializer.is_valid():
            errors = []
            for field, err_list in serializer.errors.items():
                for e in err_list:
                    errors.append(f"{field}: {e}")
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="Validation error: " + (errors[0] if errors else "Invalid dealer data"),
                details=errors,
                status_code=400,
            )

        dealer = serializer.save()
        return Response(DealerSerializer(dealer).data, status=status.HTTP_201_CREATED)


class DealerDetailView(APIView):
    def get(self, request, pk):
        try:
            dealer = Dealer.objects.get(id=pk)
        except Dealer.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Dealer with id {pk} not found",
                details=[f"Dealer {pk} does not exist"],
                status_code=404,
            )
        return Response(DealerSerializer(dealer).data)


class OrderListView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        qs = Order.objects.prefetch_related("items", "dealer").all()

        dealer_id = request.query_params.get("dealer_id")
        if dealer_id:
            qs = qs.filter(dealer_id=dealer_id)

        status_val = request.query_params.get("status")
        if status_val:
            qs = qs.filter(status=status_val)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        dealer_id = request.data.get("dealer_id")
        items_raw = request.data.get("items")
        idempotency_key = request.headers.get("Idempotency-Key")

        order = create_draft_order(
            dealer_id=dealer_id,
            items_raw=items_raw,
            idempotency_key=idempotency_key,
            raw_body=request.data,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get_object(self, order_number):
        try:
            return Order.objects.prefetch_related("items", "dealer").get(order_number=order_number)
        except Order.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Order {order_number} not found",
                details=[f"Order {order_number} does not exist"],
                status_code=404,
            )

    def get(self, request, order_number):
        order = self.get_object(order_number)
        return Response(OrderSerializer(order).data)

    def put(self, request, order_number):
        order = self.get_object(order_number)
        items_raw = request.data.get("items")
        updated_order = update_draft_order(order, items_raw)
        return Response(OrderSerializer(updated_order).data)


class OrderConfirmView(APIView):
    def post(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Order {order_number} not found",
                details=[f"Order {order_number} does not exist"],
                status_code=404,
            )
        confirmed_order = confirm_order(order)
        return Response(OrderSerializer(confirmed_order).data)


class OrderCancelView(APIView):
    def post(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Order {order_number} not found",
                details=[f"Order {order_number} does not exist"],
                status_code=404,
            )
        cancelled_order = cancel_order(order)
        return Response(OrderSerializer(cancelled_order).data)


class OrderDispatchView(APIView):
    def post(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Order {order_number} not found",
                details=[f"Order {order_number} does not exist"],
                status_code=404,
            )
        dispatched_order = dispatch_order(order)
        return Response(OrderSerializer(dispatched_order).data)


class OrderDeliverView(APIView):
    def post(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            raise CustomAPIException(
                code="NOT_FOUND",
                message=f"Order {order_number} not found",
                details=[f"Order {order_number} does not exist"],
                status_code=404,
            )
        delivered_order = deliver_order(order)
        return Response(OrderSerializer(delivered_order).data)


class ForecastView(APIView):
    def get(self, request, sku):
        from core.forecast_service import get_sku_forecast
        data = get_sku_forecast(sku)
        return Response(data)


class ReorderSuggestionsView(APIView):
    def get(self, request):
        from core.forecast_service import get_reorder_suggestions
        data = get_reorder_suggestions()
        return Response(data)


class AssistantChatView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        dealer_id = request.data.get("dealer_id")
        message = request.data.get("message")

        if not session_id or not isinstance(session_id, str):
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="session_id is required",
                details=["session_id must be a non-empty string"],
                status_code=400,
            )
        if not message or not isinstance(message, str):
            raise CustomAPIException(
                code="VALIDATION_ERROR",
                message="message is required",
                details=["message must be a non-empty string"],
                status_code=400,
            )

        from core.assistant import handle_chat
        res = handle_chat(session_id=session_id.strip(), dealer_id=dealer_id, message=message.strip())
        return Response(res)


