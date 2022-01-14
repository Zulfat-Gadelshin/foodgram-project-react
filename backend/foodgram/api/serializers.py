from rest_framework import serializers
from user.serializers import CustomUserSerializer
from .models import Tag, Ingredient, Recipe, IngredientInRecipe
#from .image_converter import Base64ImageField
from base64 import b64decode
from django.core.files.base import ContentFile
from django.http import HttpResponse
from imghdr import what
from rest_framework.serializers import ImageField
from six import string_types
from uuid import uuid4

WRONG_IMAGE_TYPE = "Изображение не соответствует"
BASE64 = ";base64,"


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, string_types):
            if "data:" in data and BASE64 in data:
                header, data = data.split(BASE64)
            try:
                decoded_file = b64decode(data)
            except TypeError:
                self.fail(WRONG_IMAGE_TYPE)
            file_name = str(uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = what(file_name, decoded_file)
        return "jpg" if extension == "jpeg" else extension

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSuccessAddSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer('tags', many=True, read_only=True)
    author = CustomUserSerializer('author', read_only=True)
    ingredients = IngredientInRecipeSerializer(source='recipe_to_ingredient', many=True, read_only=True)

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
