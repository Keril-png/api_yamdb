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
        fields = ['name', 'slug']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
#    rating = serializers.DecimalField(read_only=True, max_digits=10,
#                                      decimal_places=1, coerce_to_string=False)
    category = serializers.SlugRelatedField( 
        slug_field='slug', 
        read_only=True,  
    )
    genre = category = serializers.SlugRelatedField( 
        slug_field='slug', 
        read_only=True,  
    )
    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment