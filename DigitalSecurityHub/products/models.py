from django.db import models
from accounts.models import Seller
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Product(models.Model):
    ACTIVE_CHOICES = (
        (False, _("False")),
        (True, _("True"))
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(choices=ACTIVE_CHOICES, max_length=1, default=0)
    category = models.CharField(max_length=120)

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.price < 0:
            return
        super().save(*args, **kwargs)