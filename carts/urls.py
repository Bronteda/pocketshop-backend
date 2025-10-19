from django.urls import path
from .views import (
    MyCartView,
    ClearCartView
)

urlpatterns = [
    path("", MyCartView.as_view()), 
    path("clear/", ClearCartView.as_view()), 
]
