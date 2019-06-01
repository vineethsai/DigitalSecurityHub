from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    # path('browse', views.browse, name='browse'),
    path('<int:product_id>/review', views.productReview, name='specificProduct'),
    path(
        'review/<int:review_id>',
        views.specificProductReview,
        name='specificProductReview'
    ),
    path('', views.shop, name='shopMain')
]