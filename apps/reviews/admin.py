from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'text', 'rating')
    list_filter = ('rating', )
    search_fields = ('movie',)
    

