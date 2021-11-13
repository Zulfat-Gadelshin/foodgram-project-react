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
        fields = '__all__'
        model = Recipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = IngredientInRecipe
