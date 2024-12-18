from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id_user']
        write_only_fields = ['password']
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #  custom claims
        token['name_user'] = user.name_user
        token['type_user'] = user.type_user

        return token
