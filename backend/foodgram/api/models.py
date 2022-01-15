from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField

CustomUser = get_user_model()


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Имя Тэга')
    color = ColorField(verbose_name='Цвет Тэга')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Имя Ингридиента')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единицы измерения')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    tags = models.ManyToManyField(Tag,
                                  related_name='tags_recipes',
                                  verbose_name='Тэг рецепта')
    name = models.CharField(max_length=200, verbose_name='Имя рецепта')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    image = models.ImageField(verbose_name='Картинка',
                              upload_to='recipes', blank=True, null=True)
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), ],
        verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         through_fields=(
                                             'recipe', 'ingredient'),
                                         related_name='ingredients_recipes',
                                         blank=True,
                                         verbose_name='Ингридиенты рецепта')
    favorits = models.ManyToManyField(CustomUser,
                                      related_name='favorite_recipes',
                                      blank=True,
                                      verbose_name='У кого в избранных')
    shopping_carts = models.ManyToManyField(CustomUser,
                                            related_name='cards_recipes',
                                            blank=True,
                                            verbose_name='В списоке покупок')

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_to_ingredient',
                               verbose_name='рецепт с ингридиентом')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredient_to_recipe',
        verbose_name='ингридиенты в рецепте')
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество ингридиента')
