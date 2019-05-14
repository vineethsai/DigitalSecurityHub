from django.db import models
from auth.models import Customer
from product.models import Product

# Create your models here.
class Review(models.Model):
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)