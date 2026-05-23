from django import forms
from django.core.exceptions import ValidationError
from .models import Order
import re

class OrderCreateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'pattern': r'[\+]?[0-9]{1,3}[\s]?[0-9]{4,14}'}),
        help_text='Enter a valid Indian phone number (e.g., +91 98765 43210 or 98765 43210)'
    )
    
    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'State/Province'})
    )
    
    country = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Country name'})
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'required': True}),
            'address': forms.TextInput(attrs={'placeholder': 'Street Address', 'required': True}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'required': True}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code', 'required': True}),
        }

    def clean_phone_number(self):
        """Validate Indian phone number format"""
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove common formatting characters
            cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
            
            # Check if it starts with 91 (Indian country code)
            if cleaned.startswith('91'):
                # Remove the country code for validation
                digits_only = cleaned[2:]
            else:
                digits_only = cleaned
            
            # Indian phone numbers are 10 digits
            if not digits_only.isdigit() or len(digits_only) != 10:
                raise ValidationError(
                    'Please enter a valid Indian phone number (10 digits, e.g., +91 98765 43210 or 98765 43210).'
                )
            
            # Check if first digit of phone number is 6-9 (valid Indian mobile)
            if digits_only[0] not in ['6', '7', '8', '9']:
                raise ValidationError(
                    'Indian phone numbers should start with 6, 7, 8, or 9.'
                )
        return phone

    def clean_country(self):
        """Validate country is not empty"""
        country = self.cleaned_data.get('country')
        if country and len(country.strip()) < 2:
            raise ValidationError('Please enter a valid country name.')
        return country

    def clean_state(self):
        """Validate state is not empty"""
        state = self.cleaned_data.get('state')
        if state and len(state.strip()) < 2:
            raise ValidationError('Please enter a valid state or province.')
        return state
