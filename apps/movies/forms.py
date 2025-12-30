from django.forms import ModelForm, TextInput, Textarea
from apps.reviews.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
