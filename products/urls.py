from django.urls import path
from .views import ProductListView, ProductDetailView, ProductOrdersView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('<int:pk>/orders/', ProductOrdersView.as_view())
]
