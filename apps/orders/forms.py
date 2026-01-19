"""
Order and checkout forms.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order
from apps.users.models import Address


REGIONS = [
    ('', _('Select region')),
    ('tashkent_city', _('Tashkent City')),
    ('tashkent', _('Tashkent Region')),
    ('andijan', _('Andijan')),
    ('bukhara', _('Bukhara')),
    ('fergana', _('Fergana')),
    ('jizzakh', _('Jizzakh')),
    ('namangan', _('Namangan')),
    ('navoiy', _('Navoiy')),
    ('kashkadarya', _('Kashkadarya')),
    ('samarkand', _('Samarkand')),
    ('sirdaryo', _('Sirdaryo')),
    ('surkhandarya', _('Surkhandarya')),
    ('khorezm', _('Khorezm')),
    ('karakalpakstan', _('Karakalpakstan')),
]

CITIES = [
    ('', _('Select city')),
    ('tashkent', _('Tashkent')),
    ('andijan', _('Andijan')),
    ('bukhara', _('Bukhara')),
    ('fergana', _('Fergana')),
    ('jizzakh', _('Jizzakh')),
    ('karshi', _('Karshi')),
    ('namangan', _('Namangan')),
    ('navoiy', _('Navoiy')),
    ('nukus', _('Nukus')),
    ('samarkand', _('Samarkand')),
    ('termez', _('Termez')),
    ('urgench', _('Urgench')),
    ('guliston', _('Guliston')),
]


class CheckoutForm(forms.Form):
    """
    Checkout form with delivery and payment information.
    """

    customer_name = forms.CharField(
        max_length=200,
        label=_('Customer name'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Full Name')})
    )
    customer_email = forms.EmailField(
        label=_('Customer email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    customer_phone = forms.CharField(
        max_length=20,
        label=_('Customer phone'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 XX XXX XX XX'})
    )

    use_saved_address = forms.BooleanField(
        required=False,
        label=_('Use saved address'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    saved_address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=False,
        label=_('Saved address'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    delivery_address = forms.CharField(
        label=_('Delivery address'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    delivery_city = forms.ChoiceField(
        choices=CITIES,
        label=_('Delivery city'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    delivery_region = forms.ChoiceField(
        choices=REGIONS,
        required=False,
        label=_('Delivery region'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    latitude = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput()
    )
    longitude = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput()
    )

    payment_method = forms.ChoiceField(
        label=_('Payment method'),
        choices=Order._meta.get_field('payment_method').choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    customer_notes = forms.CharField(
        required=False,
        label=_('Customer notes'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Any special instructions?')})
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