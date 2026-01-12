from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Content
from .forms import *
from .serializers import ContentSerializer

class ContentListView(ListView):
    model = Content
    template_name = 'movies/movie_list.html'
    context_object_name = 'content_list'
    paginate_by = 12
    
    FILTER_MAPPING = {
        'q': lambda queryset, value: queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        ),
        'year': lambda queryset, value: queryset.filter(release_year=value),
        'genre': lambda queryset, value: queryset.filter(genres__slug=value),
        'actor': lambda queryset, value: queryset.filter(actors__slug=value),
    }
    
    def get_queryset(self):
        queryset = Content.objects.all()
        
        if 'series' in self.request.path:
            queryset = queryset.series()
        
        elif 'movies' in self.request.path:
            queryset = queryset.movies()
            
        for key, value in self.request.GET.items():
            if value and key in self.FILTER_MAPPING:
                queryset = self.FILTER_MAPPING[key](queryset, value)
        return queryset.distinct().order_by('-created_at')
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        if 'series' in self.request.path:
            context['page_title'] = 'Сериалы'
        
        elif 'movies' in self.request.path:
            context['page_title'] = 'Фильмы'
            
        else:
            context['page_title'] = 'Новинки кино'
        return context
    
class MovieDetailView(DetailView):
    model = Content
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'review_form' not in context:
            context['review_form'] = ReviewForm()
        return context
    
    """Запрос типа POST"""
    def post(self, request, *args, **kwargs):
        # 1. Получаем текущую страницу с фильмом
        self.object = self.get_object()
        
        # 2. Заполняем форму данными из поля ввода и кнопок
        review_form = ReviewForm(request.POST)
        
        # 3. Проверяем на валидность форму
        if review_form.is_valid():
            # 4. Создаем коментарий, но не отправляем в БД
            new_review = review_form.save(commit=False)
            
            # 5. Привязываем комментарий к странице фильма и автору
            new_review.movie = self.object
            new_review.user = request.user
            
            # 6. Сохраняем в БД
            new_review.save()
            
            # 7. Отправляем пользователя на страницу
            return redirect('movie_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(review_form=review_form))
            
class TempContentDetailView(generics.RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    
    