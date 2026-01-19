"""Review forms."""

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    images = forms.FileField(required=False)

    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'images']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-check-input'}
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summary of your review'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your experience with this product.'
            }),
        }