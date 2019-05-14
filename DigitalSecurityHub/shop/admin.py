from django.contrib import admin
from shop.models import Review, Order, LineItem, Cart

# Register your models here.
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(LineItem)
admin.site.register(Cart)