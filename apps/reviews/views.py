from django.shortcuts import render

# Create your views here.
# Содержит представления для обработки запросов API

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Review
from .serializers import *


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Review.objects.filter(movie_id=movie_id)
    
# class ReviewListView(generics.ListAPIView):
#     serializer_class = ReviewSerializer
    
#     def get_queryset(self):
#         queryset = Review.objects.all()
#         movie_id = self.request.query_params.get('movie')
    
#         if movie_id is not None:
#             queryset = queryset.filter(movie_id=movie_id)
#         return queryset
            

