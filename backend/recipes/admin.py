from django.contrib import admin

from .models import (
    Recipe, Ingredient, Tag,
    Favorite, ShoppingCart,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    search_fields = ("author",)
    list_filter = (
        "author",
        "name",
        "tags",
    )
    list_display_links = ("name",)
    readonly_fields = ('in_favorites',)

    admin.site.empty_value_display = "Не задано"

    @admin.display(description='Добавили в избранное')
    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    list_display_links = ("name",)

    admin.site.empty_value_display = "Не задано"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    list_display_links = ("name",)

    admin.site.empty_value_display = "Не задано"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)

    admin.site.empty_value_display = "Не задано"


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)

    admin.site.empty_value_display = "Не задано"
