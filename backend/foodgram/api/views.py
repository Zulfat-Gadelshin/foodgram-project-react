from rest_framework import viewsets, filters, permissions, status
from .models import *
from .serializers import *
from .filters import IngredientFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageLimitPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

User = get_user_model()


class TagViewSet(viewsets.mixins.ListModelMixin,
                 viewsets.mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.mixins.ListModelMixin,
                        viewsets.mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageLimitPagination


class FavoriteViewSet(viewsets.mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, recipe_id):
        fav = get_object_or_404(Recipe, id=recipe_id)
        user = request.user

        if user.favorite_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт уже в избранных.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user.favorite_recipes.add(fav)
        serializer = RecipeAddToFavoritesSerializer(fav, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        fav = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if not user.favorite_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт не в избранном.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.favorite_recipes.remove(fav)
        return Response(status=status.HTTP_204_NO_CONTENT)
