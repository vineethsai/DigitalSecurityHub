from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("<int:order_id>", views.specificOrder, name="specificOrder"),
    path("checkout", views.checkout, name="Checkout")    
]