from enum import unique
from django.db import models
from apps.core.models import TimeStampedModel


class Article(TimeStampedModel):

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"


    title = models.CharField(
        verbose_name='Статья',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Адрес страницы',
        max_length=100,
        unique=True
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