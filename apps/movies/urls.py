from django.contrib import admin
from django.urls import path
from .views import ContentListView, MovieDetailView, TempContentDetailView

urlpatterns = [
    path('', ContentListView.as_view(), name='home'),
    path('movies/', ContentListView.as_view(), name='movie_list'),
    path('series/', ContentListView.as_view(), name='series_list'),
    path('movie/<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/', TempContentDetailView.as_view(), name='movie-list'),
]
