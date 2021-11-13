from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from . import serializers
from .permissions import *

from .models import *


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomUserSerializer
    # authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(detail=False, methods='GET',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cur_user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(cur_user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(cur_user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(data=request.data, role=cur_user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods='POST',
            permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        pass
    # @action(detail=False, methods=('GET', 'PATCH'),
    #         permission_classes=[permissions.IsAuthenticated])
    # def set_password(self, request):
