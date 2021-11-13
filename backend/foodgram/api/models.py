from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    tags = models.ManyToManyField(Tag, related_name='tags_recipes')
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authors_recipes')
    image = models.ImageField()
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1), ])
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         through_fields=('recipe_id', 'ingredient_id'),
                                         related_name='ingredients_recipes'
                                         )
    favorits = models.ManyToManyField(CustomUser, related_name='favorite_recipes')
    shopping_carts = models.ManyToManyField(CustomUser, related_name='cards_recipes')


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
