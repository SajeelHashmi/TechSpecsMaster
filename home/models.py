from django.db import models
from django.contrib.auth.models import User

from products.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True,blank = True)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE ,null = True,blank = True)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)

class Message(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    message = models.TextField()
    subject = models.TextField(default='Others')
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name