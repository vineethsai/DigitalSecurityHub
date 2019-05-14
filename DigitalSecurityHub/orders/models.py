from django.db import models

# Create your models here.
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(required=True, decimal_places=2, max_digits=20, default=0.0)

class LineItem(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price_extended = models.DecimalField(required=True, decimal_places=2, max_digits=20, default=0.0)