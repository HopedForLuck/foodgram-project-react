from django.urls import include, path
from rest_framework import routers

from api.v1.views import IngredientViewSet, RecipesViewSet, TagViewSet
from users.views import CustomUserViewSet

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
