from rest_framework import serializers
from django.utils.html import escape
from django.db.models import Avg
from apps.movies.models import Content

class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для контента(фильмы/сериалы)"""
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = '__all__'
        
    def get_average_rating(self, object):
        average = object.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average else 0