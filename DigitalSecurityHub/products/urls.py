from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.ProductList, name="products"),
    path("<int:product_id>", views.SpecificProduct, name="SpecificProduct"),
    path("edit/<int:product_id>", views.productEdit, name="productEdit")
]