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


class IngredientInRecipeSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        fields = ('name', 'amount', 'measurement_unit')
        model = IngredientInRecipe


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer('tags', many=True)
    author = CustomUserSerializer('author')
    ingredients = IngredientInRecipeSerializer(source='recipe_to_ingredient', many=True)

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


# class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IngredientInRecipe
#         fields = ('id', 'amount')

class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    # ingredients = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=Ingredient.objects.all())
    # ingredients = IngredientInRecipeCreateSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author',
                  'name', 'image', 'text', 'cooking_time')

    # def create(self, validated_data):
    #     instance = super().create(validated_data)
    #     print(self.data['ingredients'])
    #     # for ingredient in validated_data['ingredients']:
    #     #     #IngredientInRecipe.objects.create(recipe=instance, ingredient=ingredient['id'], amount=ingredient['amount'])
    #     #     print(ingredient)
    #     return instance
