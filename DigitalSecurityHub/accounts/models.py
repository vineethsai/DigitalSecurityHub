from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.translation import ugettext_lazy as _


class Customer(models.Model):
    RELEVANCE_CHOICES = (
        (0, _("Customer")),
        (1, _("Vendor"))
    )
    customer_id = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    address = models.CharField(max_length=100, default='UDistrict')
    city = models.CharField(max_length=100, default='Seattle')
    state = models.CharField(max_length=100, default='WA')
    zip = models.IntegerField(default=98105)
    birth_date = models.DateField(default=datetime.date.today)
    type = models.CharField(choices=RELEVANCE_CHOICES, max_length=2)


class Company(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    address = models.TextField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip = models.IntegerField(default=12345)


class Seller(models.Model):
    name = models.CharField(max_length=100, default='')
    seller_id = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    # birth_date = models.DateField(default=datetime.date.today)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)





