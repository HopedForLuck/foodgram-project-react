from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

LENGTH_EMAIL = 256
LENGTH_NAME = 150
LENGTH_ROLE = 16
LENGTH_CODE = 36


class User(AbstractUser):
    """Custom User model."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=LENGTH_NAME,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LENGTH_NAME,
        blank=False,
    )
    username = models.CharField(
        max_length=LENGTH_NAME,
        verbose_name='Логин',
        unique=True,
        db_index=True,
        error_messages={
            'unique': "Пользователь с таким логином уже существует",
        },
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        verbose_name='Email адрес',
        max_length=LENGTH_EMAIL,
        unique=True,
        error_messages={
            'unique': "Пользователь с такой почтой уже существует",
        },
    )
    bio = models.TextField(
        blank=True,
        verbose_name="О пользователе",
    )
    confirmation_code = models.CharField(
        max_length=LENGTH_CODE,
        null=True,
        blank=True,
        verbose_name="Код подтверждения",
    )

    class Meta:
        ordering = ('id', )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id', )
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
