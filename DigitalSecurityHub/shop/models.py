from django.db import models
from accounts.models import Customer
from products.models import Product
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Review(models.Model):
    REVIEW_CHOICES = (
        (5, _("Amazing")),
        (4, _("Great")),
        (3, _("Good")),
        (2, _("Poor")),
        (1, _("Terrible"))
    )
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5, choices=REVIEW_CHOICES)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.rating > 5 or self.rating < 1:
            return
        super().save(*args, **kwargs)