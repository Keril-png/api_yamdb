import secrets
import string

from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .api_filters import *
from .models import *
from .permissions import *
from .serializers import *


class SendConfirmationCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        user, created = CustomUser.objects.get_or_create(
            email=email,
            username=username
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoggingUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        confirmation_code = email = serializer.data['confirmation_code']
        user = get_object_or_404(CustomUser, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminPermission]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CDLViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CDLViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class GenreViewSet(CDLViewSet):

    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__pk=title_id, pk=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__pk=title_id, pk=review_id)
        serializer.save(author=self.request.user, review=review)
