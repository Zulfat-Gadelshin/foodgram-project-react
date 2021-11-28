from rest_framework import serializers
from user.serializers import CustomUserSerializer

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSuccessAddSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer('tags', many=True)
    author = CustomUserSerializer('author')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user.favorite_recipes.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return user.cards_recipes.filter(id=obj.id).exists()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        model = Recipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredients.ingredient_id.name')
    measure_unit = serializers.FloatField(source='ingredients.ingredient_id.measure_unit')
    amount = serializers.FloatField(source='ingredients.amount')

    class Meta:
        fields = ('name', 'amount', 'measure_unit')
        model = Recipe

