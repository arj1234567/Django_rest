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
        

class GetDropdownSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='product_name')
    
    class Meta:
        model = Product
        fields = ['value','label']