from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from .filters import IngredientFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageLimitPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPageLimitPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = None
    pagination_class = CustomPageLimitPagination


class IngredientInRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientInRecipe.objects.all()
    serializer_class = IngredientInRecipeSerializer
    pagination_class = CustomPageLimitPagination
