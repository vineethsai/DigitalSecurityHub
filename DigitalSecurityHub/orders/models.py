from django.db import models
from products.models import Product
from accounts.models import Customer

# Create your models here.
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field="customer_id")
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    shipping_name = models.CharField(max_length=60)
    shipping_address = models.CharField(max_length=250)
    shipping_city = models.CharField(max_length=30)
    shipping_state = models.CharField(max_length=4)
    shipping_zip = models.IntegerField(default=12345)
    billing_name = models.CharField(max_length=60)
    billing_card = models.IntegerField(default=00000)
    billing_expiration = models.CharField(max_length=5)
    billing_cvv = models.IntegerField(default=000)

class LineItem(models.Model):
    order_id = models.ForeignKey("Order", on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price_extended = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)