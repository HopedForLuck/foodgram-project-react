from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()

LENGTH_TEXT = 20
LENGTH_NAME = 200
LENGTH_SLUG = 50


class Ingredient(models.Model):
    name = models.CharField(
        max_length=LENGTH_NAME,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=LENGTH_NAME,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Tag(models.Model):
    name = models.CharField(
        max_length=LENGTH_NAME,
        verbose_name='Название',
        unique=True,
    )
    slug = models.SlugField(
        max_length=LENGTH_SLUG,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг содержит недопустимый символ'
        )]
    )
    color = ColorField(
        verbose_name='Hex код цвета',
        unique=True,
        max_length=7,
        format="hex",
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Recipe(models.Model):
    name = models.CharField(
        max_length=LENGTH_NAME,
        verbose_name='Название',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Автор рецепта",
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name="Изображение",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Минут до готовности',
        validators=[
            MinValueValidator(
                1,
                "Время на готовку не может составлять меньше минуты",
            ),
        ],
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class IngredientRecipe(models.Model):

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, "Количество не может быть меньше одного"),
        ],
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name="recipe",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name="ingredient",
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
