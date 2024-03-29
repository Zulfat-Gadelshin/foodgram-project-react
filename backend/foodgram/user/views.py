from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from . import serializers

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.CustomUserSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.serializer_class(
                request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = self.filter_queryset(request.user.subscriptions.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CustomUserWithRecipesSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = serializers.CustomUserWithRecipesSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class SubscribeViewSet(viewsets.mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    # def create(self, request, user_id):
    def get(self, request, user_id):
        sub = get_object_or_404(User, id=user_id)
        user = request.user
        if user.id == user_id:
            content = {'errors': 'Невозможно подписаться на себя.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if user.subscriptions.filter(id=user_id).exists():
            content = {'errors': 'Вы уже подписаны на пользователя.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.subscriptions.add(sub)
        serializer = serializers.CustomUserWithRecipesSerializer(
            sub, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        sub = get_object_or_404(User, id=user_id)
        user = request.user
        if not user.subscriptions.filter(id=user_id).exists():
            content = {'errors': 'Не подписан на пользователя.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.subscriptions.remove(sub)
        return Response(status=status.HTTP_204_NO_CONTENT)
