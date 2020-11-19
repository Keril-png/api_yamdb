from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, blank=False)
    year = models.PositiveIntegerField(db_index=True, validators=[
                                       MaxValueValidator(date.today().year)])
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Genre')


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField('Комментарий оценки')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField('Дата и время публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        unique_together = ['title', 'author']

    def __str__(self):
        return self.text


class Comment(models.Model):

    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Оценка')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Автор')
    text = models.TextField('Комментарий к оценке')
    pub_date = models.DateTimeField('Дата и время публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
