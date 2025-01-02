from django.http import JsonResponse
from rest_framework import serializers
from rest_app.models import Product


class CreateProductSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True,required=False)
    product_name = serializers.CharField(allow_null=True,allow_blank=True)
    product_price = serializers.IntegerField(allow_null=True)
    product_validity = serializers.DateField(allow_null=True)
    
    class Meta:
        model = Product
        fields = ['id','product_name','product_price','product_validity']
        
    def validate(self, attrs):
        return super().validate(attrs)
        
    def create(self,validated_data):
        instance = Product()
        instance.product_name = validated_data.get('product_name',None)
        instance.product_price = validated_data.get('product_price',None)
        instance.product_validity = validated_data.get('product_validity',None)
        instance.save()
        return instance
    
    def update(self,instance,validated_data):
        instance.product_name = validated_data.get('product_name',None)
        instance.product_price = validated_data.get('product_price',None)
        instance.save()
        return instance
    

    
class DeleteProductSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField())
    
    class Meta:
        model = Product
        fields = ['id']
        
    