from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer

User = get_user_model()


#class CustomUserSerializer(serializers.ModelSerializer):
class CustomUserSerializer(UserSerializer):

    class Meta:
        fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed")
        model = User
