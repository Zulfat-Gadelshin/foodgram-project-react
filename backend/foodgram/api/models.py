from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'

    id = models.BigAutoField(primary_key=True)
    confirmation_code = models.CharField(max_length=16, verbose_name='Код')
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True, choices=Roles.choices)
    email = models.EmailField(verbose_name='email', unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    subscriptions = models.ManyToManyField("self", symmetrical=False)
    favorits = models.ManyToManyField(Recipe)
    shopping_carts = models.ManyToManyField(Recipe)


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


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
