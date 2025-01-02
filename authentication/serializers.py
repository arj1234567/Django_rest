from rest_framework import serializers
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True,allow_blank=True)
    password = serializers.CharField(allow_null=True,allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username','password']
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token':('Token is invalid or expired')
        
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return super().validate(attrs)
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')