# Определяет сериализаторы для модели Review

from rest_framework import serializers
from django.utils.html import escape
from apps.reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    class Meta:
        model = Review
        fields = ['id', 'movie', 'title', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'movie', 'created_at', 'updated_at']
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Заголовок не может быть пустым')
        return escape(value.strip())
    
    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Текст не может быть пустым')
        return escape(value.strip())
    
class ReviewCreateSerializer(ReviewSerializer):
    pass

class ReviewUpdateSerializer(ReviewSerializer):
    # Для обновления отзыва делает поля необязательными
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)