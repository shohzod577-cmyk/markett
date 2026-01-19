from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match')
        return cleaned

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError('This username is already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError('An account with this email already exists')
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
