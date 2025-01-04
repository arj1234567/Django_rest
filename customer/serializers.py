from django.http import JsonResponse
from rest_framework import serializers
from customer.models import Customer

class CreateorupdatecustomerSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True,required=False)
    customer_name = serializers.CharField(allow_null=True,allow_blank=True)
    email = serializers.CharField(allow_null=True,allow_blank=True)
    phoneno = serializers.CharField(allow_null=True,allow_blank=True)
    address = serializers.CharField(allow_null=True,allow_blank=True)
    
    class Meta:
        model = Customer
        fields = ['id','customer_name','email','phoneno','address']
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        instance = Customer()
        instance.customer_name = validated_data.get('customer_name',None)
        instance.email = validated_data.get('product',None)
        instance.phoneno = validated_data.get('phoneno',None)
        instance.address = validated_data.get('address',None)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name',None)
        instance.email = validated_data.get('product',None)
        instance.phoneno = validated_data.get('phoneno',None)
        instance.address = validated_data.get('address',None)
        instance.save()
        return  instance
    
class DeleteCustomerSerializers(serializers.ModelSerializer):
    id = serializers.ListField(child = serializers.IntegerField())
    
    class Meta:
        model = Customer
        fields = ['id']
        