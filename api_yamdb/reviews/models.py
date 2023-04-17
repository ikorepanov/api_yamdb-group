from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
   

class Category(models.Model):
    """Класс Категории."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание категории',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категорий содержит недопустимый символ!'
        )]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс Жанры."""

    name = models.CharField(
        max_length=75,
        verbose_name='Hазвание жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ!'
        )]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание произведения',
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Год не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Введеный год не может быть больше текущего'
            )
        ],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр произведения.'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name