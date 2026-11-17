from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثلاً 09123456789'
            }),
        }
        labels = {
            'phone_number': 'شماره تماس جهت پیگیری',
        }
