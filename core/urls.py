from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),
    # Products
    path("products/", views.ProductListView.as_view()),
    path("products/<str:sku>/", views.ProductDetailView.as_view()),
    # Inventory
    path("inventory/<str:sku>/", views.InventoryUpdateView.as_view()),
    # Dealers
    path("dealers/", views.DealerListView.as_view()),
    path("dealers/<int:pk>/", views.DealerDetailView.as_view()),
    # Orders
    path("orders/", views.OrderListView.as_view()),
    path("orders/<str:order_number>/", views.OrderDetailView.as_view()),
    path("orders/<str:order_number>/confirm/", views.OrderConfirmView.as_view()),
    path("orders/<str:order_number>/dispatch/", views.OrderDispatchView.as_view()),
    path("orders/<str:order_number>/deliver/", views.OrderDeliverView.as_view()),
    path("orders/<str:order_number>/cancel/", views.OrderCancelView.as_view()),
    # Forecasting & Reorder
    path("forecast/<str:sku>/", views.ForecastView.as_view()),
    path("reorder-suggestions/", views.ReorderSuggestionsView.as_view()),
    # Assistant
    path("assistant/chat/", views.AssistantChatView.as_view()),
]
