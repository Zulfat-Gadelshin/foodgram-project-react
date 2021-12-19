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
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    image = models.ImageField(verbose_name="Картинка", upload_to="recipes")
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1), ])
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         through_fields=('recipe', 'ingredient'),
                                         related_name='ingredients_recipes',
                                         blank=True,)
    favorits = models.ManyToManyField(CustomUser, related_name='favorite_recipes', blank=True)
    shopping_carts = models.ManyToManyField(CustomUser, related_name='cards_recipes', blank=True,)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_to_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_to_recipe')
    amount = models.IntegerField(validators=[MinValueValidator(1)])
