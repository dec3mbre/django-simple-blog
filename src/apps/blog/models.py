from enum import unique
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel



User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='Адрес страницы',
        max_length=50,
        unique=True
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(TimeStampedModel):

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"
        
    class Meta(TimeStampedModel.Meta):
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


    title = models.CharField(
        verbose_name='Статья',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Адрес страницы',
        max_length=100,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='articles'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='articles'
    )
    
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='blog/images/',
        null=True,
        blank=True
    )
    content = models.TextField(
        verbose_name='Статья'
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )