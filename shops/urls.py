from django.urls import path
from .views import ShopListView, ShopDetailView

urlpatterns = [
    path('', ShopListView.as_view()),
    path('<int:pk>/', ShopDetailView.as_view()),
]
