from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('new/', ProductCreateView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view())
]
