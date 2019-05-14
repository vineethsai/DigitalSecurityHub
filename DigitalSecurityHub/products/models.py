from django.db import models
from accounts.models import Seller

# Create your models here.
class Product(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    seller_id       = models.ForeignKey(Seller, on_delete=models.CASCADE)
    stock           = models.IntegerField(default=0)
    active          = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title