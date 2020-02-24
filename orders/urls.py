from django.urls import path

from . import views
from .views import ShoppingListView


urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.menu, name="menu"),
    path("services/", views.services, name="services"),
    path("order/", views.order, name="order"),
    path('shopping-cart/',  views.cart, name='shopping-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/', views.remove_from_cart, name='remove'),
    path("confirm-order-final/", views.confirm_order_final),
    path("cancel-order/", views.cancel_order),
    path("order/<int:order_id>", views.order, name="order"),
    path("orders-history/", views.orders_history, name="orders_history"),
    #path("add-to-cart", views.add_to_cart)
]
