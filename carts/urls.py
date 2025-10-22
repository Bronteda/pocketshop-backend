from django.urls import path
from .views import (
    MyCartView,
    AddCartItemView,
    ClearCartView
)

urlpatterns = [
    path("", MyCartView.as_view()), 
    path("new/", AddCartItemView.as_view()),
    path("clear/", ClearCartView.as_view()), 
]
