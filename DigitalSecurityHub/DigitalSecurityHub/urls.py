from django.contrib import admin
from django.urls import path, include

handler404 = 'DigitalSecurityHub.views.handler404'
handler500 = 'DigitalSecurityHub.views.handler500'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("products/", include("products.urls")),
    path("", include("home.urls")),
    path("home/", include("home.urls")),
    path("shop/", include("shop.urls")),
    path('api/', include('products.api.urls'))
]
