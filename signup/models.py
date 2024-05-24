from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    zipCode = models.CharField(max_length=200, null=True)