from django.db import models
from django.utils import timezone
from django.db.models import Avg

class MovieQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(average_rating=Avg('reviews__rating'))
    
    def movies(self):
        return self.filter(type='movie')
    
    def series(self):
        return self.filter(type='series')
        

class MovieManager(models.Manager):
    """Интерфейс Movie.objects"""
    def get_queryset(self):
        return MovieQuerySet(self.model, using=self._db).with_rating()
    
    def movies(self):
        return self.get_queryset().movies()
    
    def series(self):
        return self.get_queryset().series()