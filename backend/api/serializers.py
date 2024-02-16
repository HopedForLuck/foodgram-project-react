from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField

from recipes.models import (Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Subscribe

User = get_user_model()


class RecipeBaseSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


# class CustomCreateUserSerializer(UserCreateSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'password',
#         )


class SubscribeSerializer(CustomUserSerializer):
    recipes_count = SerializerMethodField()
    recipes = RecipeBaseSerializer(many=True, read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeBaseSerializer(recipes, many=True, read_only=True)
        return serializer.data


# class FavoriteRecipeSerializer(serializers.ModelSerializer):
#
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     image = Base64ImageField(
#         max_length=None,
#         use_url=False,
#     )
#     cooking_time = serializers.IntegerField()
#
#     class Meta:
#         model = Favorite
#         fields = ['id', 'name', 'image', 'cooking_time']
#         validators = UniqueTogetherValidator(
#             queryset=Favorite.objects.all(), fields=('user', 'recipe')
#         )
#
#     def validate(self, data):
#         request = self.context['request']
#         user = request.user
#         if request.method == 'POST':
#             recipe = self.context['recipe']
#             if user.favorites.filter(recipe=recipe).exists():
#                 raise serializers.ValidationError(
#                     message='Рецепт уже в избранном.'
#                 )
#
#     def create(self, validated_data):
#         return Favorite.objects.create(**validated_data).recipe


# class ShoppingCartSerializer(serializers.ModelSerializer):
#
#     def validate(self, data):
#         tags = self.initial_data.get('tags')
#         if not tags:
#             raise serializers.ValidationError('Выберите тэг')
#
#         tag_list = []
#         for tag in tags:
#             if tag in tag_list:
#                 raise serializers.ValidationError(
#                 'Тэги не могут повторяться'
#                 )
#             tag_list.append(tag)
#
#         tags_exist = Tag.objects.filter(id__in=tags)
#         if len(tags_exist) != len(tags):
#             raise ValidationError('Указан несуществующий тэг')
#
#         data['tags'] = tags
#         return data
#
#     class Meta:
#         model = ShoppingCart
#         fields = ('recipe', 'user')
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=ShoppingCart.objects.all(),
#                 fields=('recipe', 'user'),
#                 message='Рецепт уже добавлен'
#             )
#         ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeListSerializer(serializers.ModelSerializer):
    """Получение списка рецептов."""
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    author = CustomUserSerializer(read_only=True)

    def get_ingredients(self, recipe):

        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("recipe__amount")
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'ingredients',
            'is_favorited',
            'tags',
            'author',
            'is_in_shopping_cart',
            'image',
            'text',
            'cooking_time',
        )


class IngredientRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeCreateUpdateSerializer(many=True)
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        image = self.initial_data.get('image')
        if not ingredients:
            raise serializers.ValidationError('Выберите ингредиент')
        if not tags:
            raise serializers.ValidationError('Выберите тэг')
        if not image:
            raise serializers.ValidationError('Добавьте картинку к рецепту')

        tag_list = []
        for tag in tags:
            if tag in tag_list:
                raise serializers.ValidationError('Тэги не могут повторяться')
            tag_list.append(tag)

        tags_exist = Tag.objects.filter(id__in=tags)
        if len(tags_exist) != len(tags):
            raise ValidationError('Указан несуществующий тэг')

        ingredients_list = []

        for i in ingredients:
            if i["id"] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться'
                )
            if int(i['amount']) < 0:
                raise serializers.ValidationError(
                    'Количество ингредиента не может равняться нулю')
            ingredients_list.append(i["id"])

        ingredients_exist = Ingredient.objects.filter(id__in=ingredients_list)

        if len(ingredients_exist) != len(ingredients_list):
            raise ValidationError('Указан несуществующий ингредиент')

        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def recipe_ingredients_set(self, recipe, ingredients):

        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):

        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.recipe_ingredients_set(recipe=recipe, ingredients=ingredients)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                IngredientRecipe(
                    recipe=instance,
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            IngredientRecipe.objects.bulk_create(
                create_ingredients
            )
        return super().update(instance, validated_data)

    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True
        ).data
        return representation

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'ingredients',
            'tags',
            'cooking_time',
            'text',
            'author',
            'is_in_shopping_cart',
            'is_favorited',
        )
