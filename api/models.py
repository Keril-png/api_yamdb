from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    roles = (
        ('user', 'user'),
        ('moderator', 'moderator '),
        ('admin', 'admin '),
        ('django_adm', 'django_adm'),
        ('AnonymousUser', 'AnonymousUser')
    )
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=500, choices=roles, default='user')
    confirmation_code = models.CharField(max_length=10, blank=True)
    token = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.FloatField()
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField()


class Comment(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
