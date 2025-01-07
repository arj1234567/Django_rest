from django.shortcuts import render
import os
import sys
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.pagination import PageNumberPagination
from rest_project.helpers.pagination import RestPagination
from rest_project.helpers.response import ResponseInfo
from customer.models import Customer
from customer.serializers import CreateorupdatecustomerSerializers,DeleteCustomerSerializers
from customer.schemas import GetCustomerListSchemas,GetCustomerDropdownSchemas


class CreateorupdateCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateorupdateCustomerApiView, self).__init__(**kwargs)
    serializer_class = CreateorupdatecustomerSerializers
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=['Customer'])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={
                'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            customer_id = serializer.validated_data.get('id', None)
            customer_instance = Customer.objects.filter(id=customer_id).first() if customer_id else None

            serializer = self.serializer_class(
                customer_instance, data=request.data, context={'request': request}
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
        
        
class CustomerlistApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CustomerlistApiView,self).__init__(**kwargs)
        
    serializer_class = GetCustomerListSchemas
    permission_classes = (IsAuthenticated,)
    pagination_class = RestPagination
    
    @swagger_auto_schema(tags=['Customer'])
    def get(self,request):
        try:
            queryset = Customer.objects.all().order_by('-id')
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
        
        
class GetCustomerDetailsApiViiew(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetCustomerDetailsApiViiew).__init__(**kwargs)
        
    serializer_class = GetCustomerListSchemas
    permission_classes = (IsAuthenticated,)
    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="Enter customer id",required=True)
    
    
    @swagger_auto_schema(tags=['Customer'],manual_parameters=[id])
    def get(self,request):
        try:
            customer_id = request.GET.get('id',None)
            customer_instance = Customer.objects.get(id=customer_id)
            if customer_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format['messsage'] = 'record not found'
                self.response_format['status'] = False
                return Response(self.response_format,status=status.HTTP_204_NO_CONTENT)
            
            serializer = self.serializer_class(customer_instance,context={'request':request})
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format['data'] = serializer.data
            self.response_format['message'] = 'success'
            self.response_format['status'] = False 
            return Response(self.response_format,status=status.HTTP_200_OK)
        except Exception as e:
            exc_type,exc_obj,exc_tb                       = sys.exc_info()
            fname                                         = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']           = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                = False
            self.response_format['message']               = f'exc_type:{exc_type},fname:{fname},tb_lineno:{exc_tb.tb_lineno},error:{str(e)}'
            return Response(self.response_format,status   = status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
        
class DeleteCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteCustomerApiView).__init__(**kwargs)
        
    serializer_class = DeleteCustomerSerializers
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=['Customer'],request_body=serializer_class)
    def delete(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
            ids = serializer.validated_data.get('id',None)
            Customer.objects.get(id__in = ids).delete()
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format['message'] = 'success'
            self.response_format['status'] = True
            return Response(self.response_format,status=status.HTTP_200_OK)
        
        except Exception as e: 
            exc_type, exc_obj, exc_tb                       = sys.exc_info()
            fname                                           = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCustomerDropdownApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetCustomerDropdownApiView).__init__(**kwargs)
        
    serializer_class = GetCustomerDropdownSchemas
    pagination_class = (IsAuthenticated,)
    pagination_class = RestPagination
    
    @swagger_auto_schema(tags=['Customer'])
    def get(self,request):
        try:
            queryset = Customer.objects.all().order_by('-id')
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(page,many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)
        
        except Exception as e: 
            exc_type, exc_obj, exc_tb                       = sys.exc_info()
            fname                                           = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
# Create your views here.
