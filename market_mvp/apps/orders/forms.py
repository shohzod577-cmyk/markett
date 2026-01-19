from django import forms


class OrderCreateForm(forms.Form):
    first_name = forms.CharField(max_length=120, required=True)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False)
    address_line1 = forms.CharField(max_length=255, required=True)
    address_line2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=120, required=False)
    postal_code = forms.CharField(max_length=30, required=False)
    country = forms.CharField(max_length=80, required=False, initial='Uzbekistan')
