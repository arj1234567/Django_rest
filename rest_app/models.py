from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255,null=True,blank=True)
    product_price = models.IntegerField(null=True)
    product_validity = models.DateTimeField(null=True,blank=True)
    product_status = models.BooleanField(default=True)
    
# Create your models here.
