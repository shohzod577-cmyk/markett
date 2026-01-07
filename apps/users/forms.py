"""
User forms for authentication and profile management.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Address

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    User registration form with password confirmation.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 XX XXX XX XX'
            }),
        }

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean(self):
        """Validate password confirmation."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords do not match.')

        return cleaned_data


class UserLoginForm(forms.Form):
    """
    User login form.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    User profile update form.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar', 'preferred_currency']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'preferred_currency': forms.Select(attrs={'class': 'form-select'}),
        }


class AddressForm(forms.ModelForm):
    """
    Address form with geolocation support.
    """

    class Meta:
        model = Address
        fields = [
            'label', 'full_address', 'city', 'region',
            'postal_code', 'phone', 'latitude', 'longitude', 'is_default'
        ]
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Home, Office'
            }),
            'full_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Full address'
            }),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }