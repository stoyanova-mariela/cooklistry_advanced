from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating',
            'comment': 'Your review',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Enter a rating from 1 to 5'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience with this recipe...'}),
        }
        help_texts = {
            'rating': 'Rate this recipe from 1 to 5.',
            'comment': 'Maximum 500 characters.',
        }
        error_messages = {
            'rating': {
                'required': 'Please enter a rating.',
                'min_value': 'The rating must be at least 1.',
                'max_value': 'The rating cannot be greater than 5.',
                'invalid': 'Please enter a valid whole number.',
            },
            'comment': {
                'required': 'Please write a review.',
                'max_length': 'Your review cannot exceed 500 characters.',
            },
        }
