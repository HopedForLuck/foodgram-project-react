from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint

LENGTH_EMAIL = 256
LENGTH_USERNAME = 150
LENGTH_ROLE = 16
LENGTH_CODE = 36


class User(AbstractUser):
    """Custom User model."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь")
    ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'password',
    ]

    username = models.CharField(
        max_length=LENGTH_USERNAME,
        verbose_name='Имя пользователя',
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
    role = models.CharField(
        max_length=LENGTH_ROLE,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )
    confirmation_code = models.CharField(
        max_length=LENGTH_CODE,
        null=True,
        blank=True,
        verbose_name="Код потдверждения",
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

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
        related_name='subscribe_to',
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id', )
        constraints = [
            UniqueConstraint(fields=['user', 'author'], name='unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
