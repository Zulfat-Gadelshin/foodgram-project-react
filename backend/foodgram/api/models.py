from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.URLField()
    text = models.CharField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         through_fields=('recipe_id', 'ingredient_id'),
                                         )
    favorits = models.ManyToManyField(CustomUser)
    shopping_carts = models.ManyToManyField(CustomUser)


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
