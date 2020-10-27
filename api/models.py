from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


#User = get_user_model()


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
    year = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles_of_category",
        blank=True,
        null=True,
    )
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
    pub_date = models.DateTimeField('Дата и время', auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        ordering = ['-pub_date']
        unique_together = ['title', 'author']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Оценка'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField('Комментарий к оценке')
    pub_date = models.DateTimeField('Дата и время', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']