from rest_framework import serializers

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):


    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  #'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        model = Recipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = IngredientInRecipe
