from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField


CustomUser = get_user_model()


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    color = ColorField()
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    tags = models.ManyToManyField(Tag, related_name='tags_recipes')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authors_recipes')
    image = models.ImageField(blank=True, null=True)
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1), ])

    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         through_fields=('recipe_id', 'ingredient_id'),
                                         related_name='ingredients_recipes',
                                         blank=True,)
    favorits = models.ManyToManyField(CustomUser, related_name='favorite_recipes', blank=True)
    shopping_carts = models.ManyToManyField(CustomUser, related_name='cards_recipes', blank=True,)


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
