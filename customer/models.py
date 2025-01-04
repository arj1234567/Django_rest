from django.db import models

class Customer(models.Model): 
    customer_name               = models.CharField(max_length=255,null=True,blank=True)
    email                       = models.CharField(max_length=255,null=True,blank=True)
    phoneno                     = models.CharField(max_length=255,null=True,blank=True)
    address                     = models.TextField(null=True,blank=True)
# Create your models here.
