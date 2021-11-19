from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from djoser.views import UserViewSet
#import djoser
from . import serializers
from .permissions import *

from .models import *


User = get_user_model()


class UserViewSet(UserViewSet):
    #serializer_class = serializers.CustomUserSerializer
    # authentication_classes = (authentication.JWTAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsAdmin)
    #pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()
        return queryset

