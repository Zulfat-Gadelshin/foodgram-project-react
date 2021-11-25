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
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cur_user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(cur_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
