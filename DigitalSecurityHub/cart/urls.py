from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.cart, name='cart'),
]