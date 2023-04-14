from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


# роли пользователей
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

# cписок для выбора роли
USER_ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN)
]


class User(AbstractUser):
    '''Расширяем модель User'''
    username = models.SlugField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Имя пользователя',
        help_text=(
            'Логин должен содержать только буквы и цифры.'
            ' Поле не может состоять из "me", содержать пробелы, слеши.')
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        blank=True,
        verbose_name='Роль пользователя.'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия пользователя'
    )
    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='Код подтверждения для регистрации',
        blank=False,
        default='cha-cha-cha'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username',
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
