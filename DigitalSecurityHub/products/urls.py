from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('products', views.ProductList, name='products'),
    path('/<int:product_id>', views.SpecificProduct, name='SpecificProduct')
]