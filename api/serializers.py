from rest_framework import serializers
from django.db.models import Avg
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role"
        )


class UserCreationSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=200)
    
        
class LoggingUserSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=200)


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
    rating = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True, ) 
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, title):
        avg = title.reviews.aggregate(Avg('score'))
        return avg['score__avg']


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
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(slug_field='pk', read_only='True')
    author = serializers.SlugRelatedField(slug_field='username', read_only='True')

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    review = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
