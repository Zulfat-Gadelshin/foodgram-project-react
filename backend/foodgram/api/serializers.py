from rest_framework import serializers
from user.serializers import CustomUserSerializer
from .models import Tag, Ingredient, Recipe, IngredientInRecipe
from .image_converter import Base64ImageField


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientInRecipeSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = IngredientInRecipe


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer('tags', many=True, read_only=True)
    author = CustomUserSerializer('author', read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='recipe_to_ingredient', many=True, read_only=True)
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        if hasattr(self.context.get('request'), 'user'):
            user = self.context.get('request').user
            if user.is_authenticated:
                return user.favorite_recipes.filter(id=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if hasattr(self.context.get('request'), 'user'):
            user = self.context.get('request').user
            if user.is_authenticated:
                return user.cards_recipes.filter(id=obj.id).exists()
        return False

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        model = Recipe

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["image"] = obj.image.url
        return data


class RecipeSuccessAddSerializer(RecipeSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
