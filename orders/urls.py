from django.urls import path
from .views import OrderDetailView, OrdersListView, OrdersByBuyer, OrdersForProductsByShop

urlpatterns = [
    path("", OrdersListView.as_view()),
    path("buyer/", OrdersByBuyer.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("shop/products/", OrdersForProductsByShop.as_view())
]
