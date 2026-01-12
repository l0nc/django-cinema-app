from django.contrib import admin
from .models import Content, Genre, Person

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'birth_date')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Content)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'release_year', 'slug', 'duration', 'created_at')
    list_filter = ('release_year', 'genres', 'type')
    search_fields = ('name', 'description ')
    filter_horizontal = ('genres', 'actors', 'directors')
    prepopulated_fields = {'slug': ('name',)}


