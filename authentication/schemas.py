from rest_framework import serializers
from authentication.models import User

class LoginResponseSchema(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phoneno",
            "is_admin",
        ]

