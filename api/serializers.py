from rest_framework import serializers

from .models import *


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',)
        model = CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = 'slug'
        fields = ['name', 'slug']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, ) 
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleEditSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False,
    )
    genre = serializers.SlugRelatedField( 
        queryset=Genre.objects.all(), 
        slug_field='slug',
        many=True 
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment