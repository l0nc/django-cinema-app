from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.mixins import AutoSlugMixin
from .managers import MovieManager

    
class Genre(AutoSlugMixin, TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        
    def __str__(self):
        return self.name
        
class Person(AutoSlugMixin, TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    photo = models.ImageField(upload_to='persons/', null=True, blank=True, verbose_name='Photo')
    bio = models.TextField(blank=True, verbose_name='Biography')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birthday')
    
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        
    def __str__(self):
        return self.name


class Movie(AutoSlugMixin, TimeStampedModel):
    
    MOVIE = 'movie'
    SERIES = 'series'
    TYPE_CHOICES = [
        (MOVIE, 'Фильм'),
        (SERIES, 'Сериал'),
    ]
    
    
    name = models.CharField(max_length=100, verbose_name="Name")
    
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=MOVIE,
        verbose_name='Тип'
    )
    
    seasons_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество сезонов',
        blank=True,
        null=True
    )
    
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(max_length=500, verbose_name="Description")
    release_year = models.PositiveIntegerField(verbose_name="Release year")
    poster = models.ImageField(upload_to='movies/posters', verbose_name="Poster")
    duration = models.PositiveIntegerField(verbose_name="Duration (minutes)")
    genres = models.ManyToManyField(Genre, related_name="movies", verbose_name="Genres")
    
    directors = models.ManyToManyField(
        Person,
        related_name='directed_movies',
        verbose_name="Режиссеры"
    )
    actors = models.ManyToManyField(
        Person,
        related_name='actors_movies',
        verbose_name='Актеры'
    )
    
    objects = MovieManager()
    
    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['-release_year']

    def __str__(self):
        return self.name
    
        