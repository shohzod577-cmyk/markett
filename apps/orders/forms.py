"""
Order and checkout forms.
"""
from django import forms
from .models import Order
from apps.users.models import Address


class CheckoutForm(forms.Form):
    """
    Checkout form with delivery and payment information.
    """

    # Customer information
    customer_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    customer_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 XX XXX XX XX'})
    )

    # Delivery address
    use_saved_address = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    saved_address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    delivery_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    delivery_region = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Geolocation
    latitude = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput()
    )
    longitude = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput()
    )

    # Payment method
    payment_method = forms.ChoiceField(
        choices=Order._meta.get_field('payment_method').choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    # Notes
    customer_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions?'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['saved_address'].queryset = Address.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        use_saved_address = cleaned_data.get('use_saved_address')
        saved_address = cleaned_data.get('saved_address')
        delivery_address = cleaned_data.get('delivery_address')

        if use_saved_address and not saved_address:
            raise forms.ValidationError('Please select a saved address.')

        if not use_saved_address and not delivery_address:
            raise forms.ValidationError('Please provide a delivery address.')

        return cleaned_data