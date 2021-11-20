from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from djoser.views import UserViewSet
#import djoser
from . import serializers
from .permissions import *
from rest_framework_simplejwt.tokens import RefreshToken


from .models import *


User = get_user_model()


class UserViewSet(UserViewSet):
    serializer_class = serializers.CustomUserSerializer
    # authentication_classes = (authentication.JWTAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()


# class AuthTokenViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserTokenSerializer
#     authentication_classes = None
#     permission_classes = None
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid()
#         email = serializer.data.get('email')
#         password = serializer.data.get('password')
#         if not User.objects.filter(email=email,
#                                    password=password).exists():
#             error = {
#                 "error": [
#                     "HTTP_400_BAD_REQUEST"
#                 ]
#             }
#             return Response(error,
#                             status=status.HTTP_400_BAD_REQUEST)
#         user = User.objects.filter(email=email, password=password).first()
#         token = get_tokens_for_user(user)
#
#         return Response(token,
#                         status=status.HTTP_201_CREATED)
