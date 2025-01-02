import os
import sys
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,status
from rest_app.models import Product
from rest_app.serializers import CreateProductSerializers,DeleteProductSerializer
from rest_project.helpers.response import ResponseInfo
from rest_app.schemas import GetProductListSchemas,GetProductDetailSchemas
from rest_framework.pagination import PageNumberPagination
from rest_project.helpers.pagination import RestPagination



class CreateProductApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateProductApiView, self).__init__(**kwargs)
    serializer_class = CreateProductSerializers
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=['Product'])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={
                'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            product_id = serializer.validated_data.get('id', None)
            product_instance = Product.objects.filter(id=product_id).first() if product_id else None

            serializer = self.serializer_class(
                product_instance, data=request.data, context={'request': request}
            )
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format['message'] = 'success'
            self.response_format['status'] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = (f'exc_type :{exc_type}, fname:{fname}, tb_lineno:{exc_tb.tb_lineno}, error:{str(e)}')
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetProductApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetProductApiView,self).__init__(**kwargs)
    
    serializer_class = GetProductListSchemas
    permission_classes = (IsAuthenticated,)
    pagination_class = RestPagination
    
    @swagger_auto_schema(tags=['Product'])
    def get(self,request):
        try:
            queryset = Product.objects.all().order_by('-id')
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(page,many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)
        except  Exception as e:
            exc_type,exc_obj,exc_tb                       = sys.exc_info()
            fname                                         = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']           = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                = False
            self.response_format['message']               = f'exc_type:{exc_type},fname:{fname},tb_lineno:{exc_tb.tb_lineno},error:{str(e)}'
            return Response(self.response_format,status   = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class GetProductDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetProductDetailApiView,self).__init__(**kwargs)
        
    serializer_class = GetProductDetailSchemas
    permission_classes = (IsAuthenticated,)
    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="Enter product id",required=True)
    
    @swagger_auto_schema(tags=['Product'],manual_parameters=[id])
    def get(self,request):
        try:
            product_id = request.GET.get('id',None)
            
            product_instance = Product.objects.get(id=product_id)
            if product_instance  is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format['message'] = 'record not found'    
                self.response_format['status'] = False
                return Response(self.response_format,status=status.HTTP_204_NO_CONTENT)
            serializer = self.serializer_class(product_instance,context={'request':request})
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format['data'] = serializer.data
            self.response_format['message'] = 'success'
            self.response_format['status'] = True
            return Response(self.response_format,status=status.HTTP_200_OK)
        except Exception as e:
            exc_type,exc_obj,exc_tb                       = sys.exc_info()
            fname                                         = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']           = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                = False
            self.response_format['message']               = f'exc_type:{exc_type},fname:{fname},tb_lineno:{exc_tb.tb_lineno},error:{str(e)}'
            return Response(self.response_format,status   = status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
class DeleteProductApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteProductApiView,self).__init__(**kwargs)
        
    serializer_class = DeleteProductSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=['Product'],request_body=serializer_class)
    def delete(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
            ids = serializer.validated_data.get('id',None)
            Product.objects.get(id__in=ids).delete()
            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = 'success'
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
        
        except Exception as e: 
            exc_type, exc_obj, exc_tb                       = sys.exc_info()
            fname                                           = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)

        

# Create your views here.
