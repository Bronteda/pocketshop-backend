from django.urls import path
from .views import ShopListView, ShopDetailView, UserShopView

urlpatterns = [
    path('', ShopListView.as_view()),
    path('<int:pk>/', ShopDetailView.as_view()),
    # This will get you the shop for this user
    path('owner/', UserShopView.as_view())
]
