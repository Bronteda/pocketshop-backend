from django.urls import path
from .views import OrderDetailView, OrdersListView, OrdersByBuyer

urlpatterns = [
    path("", OrdersListView.as_view()),
    path("OrdersByBuyer/", OrdersByBuyer.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
]
