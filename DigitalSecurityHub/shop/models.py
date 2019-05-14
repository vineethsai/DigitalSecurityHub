from django.db import models
from accounts.models import Customer
from products.models import Product

# Create your models here.
class Review(models.Model):
    REVIEW_CHOICES = (
        'Verified Purchaser',
        'Unverified User'
    )
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if rating > 5 or rating < 1:
            return
        super().save(*args, **kwargs)