from django.db import models
from apps.core.models import TimeStampedModel
from config.settings import AUTH_USER_MODEL
from apps.movies.models import Movie

class Review(TimeStampedModel):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Контент'
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        choices=[(i, str(i)) for i in range(1, 11)]
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} на {self.movie.name}"
