from django.urls import include, path
from rest_framework import routers

# from api.v1.views import (
#     CategoryViewSet, GenreViewSet,
#     TitleViewSet, CommentViewSet, ReviewViewSet
# )
# from users.views import (
#     UsersViewSet, SignUpViewSet,
#     GetTokenViewSet, MeProfileViewSet
# )

router = routers.DefaultRouter()

# router.register('categories', CategoryViewSet, basename='categories')
# router.register('genres', GenreViewSet, basename='genres')
# router.register('titles', TitleViewSet, basename='titles')
# router.register('auth/signup', SignUpViewSet, basename='auth')
# router.register('users', UsersViewSet, basename='users')
# router.register(
#     r"titles/(?P<title_id>\d+)/reviews",
#     ReviewViewSet,
#     basename="reviews")
# router.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet,
#     basename="comments")

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # Работа с пользователями
    path('', include('djoser.urls.authtoken')),  # Работа с токенами
]
