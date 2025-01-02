from rest_framework import serializers
from rest_app.models import Product
 
class GetProductListSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','product_name','product_price']
        

class GetProductDetailSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','product_name','product_price']