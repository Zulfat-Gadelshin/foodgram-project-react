from rest_framework import viewsets, filters, permissions, status
from .models import *
from .serializers import *
from .filters import IngredientFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageLimitPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


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

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        cur_user = request.user
        serializer = IngredientInRecipeSerializer(cur_user.cards_recipes.all(), context={'request': request}, many=True)
        # serializer = RecipeSerializer(cur_user.cards_recipes.all(),context={'request': request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK, content_type='text/plain')


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
        serializer = RecipeSuccessAddSerializer(fav, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        fav = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if not user.favorite_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт не в избранном.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.favorite_recipes.remove(fav)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, recipe_id):
        shop = get_object_or_404(Recipe, id=recipe_id)
        user = request.user

        if user.cards_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт уже в списке покупок.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user.cards_recipes.add(shop)
        serializer = RecipeSuccessAddSerializer(shop, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        shop = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if not user.cards_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт не списке покупок.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.cards_recipes.remove(shop)
        return Response(status=status.HTTP_204_NO_CONTENT)


