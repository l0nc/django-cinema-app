from django.urls import path
from .views import *
app_name = 'reviews'

urlpatterns = [
    path('movies/<int:movie_id>/reviews', ReviewListView.as_view(), name='review-list')
]