from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


api_router = DefaultRouter()
api_router.register(r'users', UserViewSet, basename='customuser')
api_router.register(r'categories', CategoryViewSet, basename='categories')
api_router.register(r'genres', GenreViewSet, basename='genres')
api_router.register(r'titles', TitleViewSet, basename='titles')
api_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
api_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(api_router.urls)),
    path('auth/email/', SendConfirmationCodeView.as_view()),
    path('auth/token/', GetTokenAPIView.as_view()),

]
