
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('jwt_auth.urls')),
    path('api/shops/', include('shops.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls'))
]