from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .filters import TitleFilter
from .models import Category, Genre, Title, Review, Comment
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .viewsets import CustomViewset

@api_view(['GET', 'POST'])