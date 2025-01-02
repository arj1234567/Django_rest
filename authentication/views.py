from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics,status
from rest_framework.response import Response
from django.contrib import auth
from django.utils import timezone
from authentication.schemas import LoginResponseSchema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from authentication.models import GeneratedAccessToken
from authentication.serializers import LoginSerializer,LogoutSerializer
from rest_project.helpers.response import ResponseInfo
from typing import Any
from rest_framework.permissions import IsAuthenticated
from rest_project.helpers.helper import get_token_user_or_none
from rest_project.middleware.JWTAuthentication import BlacklistedJWTAuthentication


class LoginApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LoginApiView, self).__init__(**kwargs)
    serializer_class = LoginSerializer
    
    @swagger_auto_schema(tags=['Authorization'])
    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            user = auth.authenticate(
                username = serializer.validated_data.get('username',""),
                password = serializer.validated_data.get('password',""),
            )
            if user:
                user.is_logged_in = True
                user.last_login = timezone.now()
                user.save()
                serializer = LoginResponseSchema(user,context={'request':request})
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                data = {
                    'user': serializer.data,
                    'token':token,
                    'refresh':str(refresh)
                }
                GeneratedAccessToken.objects.create(user=user,token=token)
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['status'] = True
                self.response_format['data'] = data
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                # Invalid credentials case
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = "Invalid credentials. Please try again."
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as es:
            # Handle any server-side errors
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(es)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LogoutApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutApiView,self).__init__(**kwargs)
    
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BlacklistedJWTAuthentication]
    
    @swagger_auto_schema(tags=['Authorization'])
    def post(self,request):
        try:
            user = get_token_user_or_none(request)
            if user is not None:
                GeneratedAccessToken.objects.filter(user=user).delete()
                user.save()
                
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format['status'] = True
                self.response_format['message'] = "Succesfully logged out"
                return Response(self.response_format,status=status.HTTP_200_OK)
                        
        except Exception as es:
            # Handle any server-side errors
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(es)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
        

            
                
                
        
# Create your views here.
