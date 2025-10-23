from django.urls import path
from .views import PaymentListView, PaymentDetailView, CheckoutView

urlpatterns = [
    path('', PaymentListView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('<int:pk>/', PaymentDetailView.as_view())
]
