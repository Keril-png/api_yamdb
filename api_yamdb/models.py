from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length = 200)
    year = models.PositiveIntegerField(default=0)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name = 'titles',
        blank=True,
        null=True,
        verbose_name = 'Заголовок'   
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name = 'categories',
        blank=True,
        null=True,
        verbose_name = 'Категория'   
    )
    
    def __str__(self):
        return self.name