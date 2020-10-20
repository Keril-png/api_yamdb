from django.shortcuts import render

import string
import secrets
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, status, filters, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import CustomUser
from .permissions import IsStaffOrAdmin
from .models import *
from .serializers import *



class EmailValidView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        alphabet = string.ascii_letters + string.digits
        confirmation_code = ''.join(secrets.choice(alphabet) for i in range(8))
        email = request.data.get('email')

        if email and (CustomUser.objects.filter(email=email).count() != 1):
            CustomUser.objects.create(email=email,
                                      confirmation_code=confirmation_code, username=email)
            send_mail(
                'Тема письма',
                f'Ваш код подтверждения {confirmation_code}.',
                'api_yamdb@mail.com',
                [email],
                fail_silently=False,
            )
            serializer = EmailSerializer(CustomUser.objects.get(email=email))
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JwtGetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self):
        email = self.request.data.get('email')
        confirmation_code = self.request.data.get('confirmation_code')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        try:
            user = CustomUser.objects.get(email=email, confirmation_code=confirmation_code)
        except ObjectDoesNotExist:
            return Response('Пары email - код подтверждения не существует', status=status.HTTP_400_BAD_REQUEST)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user_details = {}
        user_details['token'] = token
        return Response(user_details, status=status.HTTP_200_OK)


class MeView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        usr = CustomUser.objects.get(email=self.request.user.email)
        serializer = self.get_serializer(usr)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update(self, *args, **kwargs):
        usr = CustomUser.objects.get(email=self.request.user.email)
        serializer = CustomUserSerializer(usr, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UsernameView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsStaffOrAdmin,)
    lookup_field = 'username'

    def update(self, *args, **kwargs):
        try:
            usr = CustomUser.objects.get(username=self.kwargs.get('username'))
        except ObjectDoesNotExist:
            return Response(f'Пользователя не существует', status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(usr, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)



class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrAdmin | IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        if self.queryset.filter(slug=slug):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def destroy(self, request, slug=None):
        del_category = self.queryset.filter(slug=slug)
        del_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet): 

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrAdmin | IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        if self.queryset.filter(slug=slug):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def destroy(self, request, slug):
        del_genre = self.queryset.filter(slug=slug)
        del_genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsStaffOrAdmin, ]
#    filter_backends = [DjangoFilterBackend]
#    filterset_fields = ['category', 'genre', 'name', 'year']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Filter comments by post"""
        return self.queryset.filter(title_id=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Filter comments by post"""
        return self.queryset.filter(title_id=self.kwargs.get('title_id'), review_id=self.kwargs.get('review_id'))