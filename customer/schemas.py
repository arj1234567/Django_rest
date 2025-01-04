from rest_framework import serializers
from customer.models import Customer

class GetCustomerListSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id','customer_name','email','address','phoneno']
        
        
    