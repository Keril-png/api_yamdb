from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

api_router = DefaultRouter()
api_router.register('users', UserViewSet, basename='customuser')
api_router.register('categories', CategoryViewSet, basename='categories')
api_router.register('genres', GenreViewSet, basename='genres')
api_router.register('titles', TitleViewSet, basename='titles')
api_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet,
    basename='comments')

auth_urls = [
    path('email/', SendConfirmationCodeView.as_view()),
    path('token/', GetTokenAPIView.as_view())
]

urlpatterns = [
    path('', include(api_router.urls)),
    path('auth/', include(auth_urls)),
]
