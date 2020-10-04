from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False, read_only=True,)
    genre = GenresSerializer(many=True, read_only=True,)

    class Meta:
        model = Titles
        fields = '__all__'