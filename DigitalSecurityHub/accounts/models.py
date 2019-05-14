from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=40, default="")
    state = models.CharField(max_length=2, default="WA")
    zip = models.IntegerField()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)

class Company(models.Model):
    name = models.CharField(max_length=40, unique=True)
    address = models.TextField()