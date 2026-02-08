from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    """Абстрактная модель, добавляющая дату создания и обновления."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True  # Django не создаст таблицу для этой модели, это только "чертеж"


class UserProfile(models.Model):
    """Профиль пользователя с дополнительной информацией."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        default='',
    )
    github = models.CharField(
        verbose_name='GitHub',
        max_length=100,
        blank=True,
        default='',
    )
    twitter = models.CharField(
        verbose_name='Twitter',
        max_length=100,
        blank=True,
        default='',
    )
    website = models.URLField(
        verbose_name='Сайт',
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'


class Subscriber(models.Model):
    """Подписчик на рассылку."""
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
