from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for creating and editing product reviews"""
    
    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        help_text="Rate this product from 1 to 5 stars"
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Share your experience with this product...',
            'class': 'form-control'
        }),
        required=False,
        label='Your Review'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating',
            'comment': 'Review (optional)',
        }
