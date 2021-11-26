from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from djoser.views import UserViewSet
from . import serializers
from .permissions import *
from django.shortcuts import get_object_or_404

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

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = self.filter_queryset(request.user.subscriptions.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscribeViewSet(viewsets.mixins.CreateModelMixin,
                       viewsets.mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, user_id):
        sub = get_object_or_404(User, id=user_id)
        user = request.user
        print(user.subscriptions.filter(id=user_id))
        if user.id == user_id:
            content = {'errors': 'Невозможно подписаться на себя.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if user.subscriptions.filter(id=user_id).exists():
            content = {'errors': 'Вы уже подписаны на пользователя.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.subscriptions.add(sub)
        serializer = serializers.CustomUserSerializer(sub)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
