from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактная модель, добавляющая дату создания и обновления."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True  # Django не создаст таблицу для этой модели, это только "чертеж"

