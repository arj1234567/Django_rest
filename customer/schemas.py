from rest_framework import serializers
from customer.models import Customer

class GetCustomerListSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id','customer_name','email','address','phoneno']
        
        
class GetCustomerDropdownSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='customer_name')
    
    class Meta:
        model = Customer
        fields = ['value','label']
        
        
        
    