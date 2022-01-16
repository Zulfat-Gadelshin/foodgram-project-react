from rest_framework import viewsets, permissions, status
from .models import Ingredient, Recipe, IngredientInRecipe, Tag
from django.contrib.auth import get_user_model
from .serializers import IngredientSerializer
from .serializers import TagSerializer, RecipeSerializer
from .serializers import CreateRecipeSerializer, RecipeSuccessAddSerializer
from django.db import transaction

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPageLimitPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import FileResponse
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
    filter_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageLimitPagination
    # permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    filter_class = RecipeFilter

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        if request.data['ingredients'] is not None:
            ingredient_list = [IngredientInRecipe(
                recipe=serializer.instance,
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                amount=ingredient['amount'])
                for ingredient in request.data['ingredients']]
            IngredientInRecipe.objects.bulk_create(ingredient_list)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CreateRecipeSerializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        IngredientInRecipe.objects.filter(recipe=serializer.instance).delete()
        if request.data['ingredients'] is not None:
            ingredient_list = [IngredientInRecipe(
                recipe=serializer.instance,
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                amount=ingredient['amount'])
                for ingredient in request.data['ingredients']]
            IngredientInRecipe.objects.bulk_create(ingredient_list)

        return Response(serializer.data)

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        cur_user = request.user
        serializer = RecipeSerializer(
            cur_user.cards_recipes.all(),
            context={'request': request}, many=True)
        shoping_cart = []
        ingridients_name = []
        for recipe in serializer.data[:]:
            for ingredient in recipe['ingredients']:
                if ingredient['name'] in ingridients_name:
                    number = ingridients_name.index(ingredient['name'])
                    shoping_cart[number]['amount'] += ingredient['amount']
                else:
                    ingridients_name.append(ingredient['name'])
                    shoping_cart.append(ingredient)
        shoping_list = open('shopping_list.txt', 'w+', encoding='utf-8')
        for i in shoping_cart:
            shoping_list.write(
                f'{i["name"]} {(i["amount"])} {i["measurement_unit"]}\n')
        shoping_list.close()
        shoping_list = open('shopping_list.txt', 'rb')
        return FileResponse(shoping_list, content_type='text/plain')


class FavoriteViewSet(viewsets.mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, recipe_id):
        fav = get_object_or_404(Recipe, id=recipe_id)
        user = request.user

        if user.favorite_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт уже в избранных.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user.favorite_recipes.add(fav)
        serializer = RecipeSuccessAddSerializer(
            fav, context={'request': request})
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

    def get(self, request, recipe_id):
        shop = get_object_or_404(Recipe, id=recipe_id)
        user = request.user

        if user.cards_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт уже в списке покупок.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user.cards_recipes.add(shop)
        serializer = RecipeSuccessAddSerializer(
            shop, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        shop = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if not user.cards_recipes.filter(id=recipe_id).exists():
            content = {'errors': 'Рецепт не списке покупок.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user.cards_recipes.remove(shop)
        return Response(status=status.HTTP_204_NO_CONTENT)
