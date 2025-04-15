from django import forms
from wishlist.models import *


class LoginForm(forms.Form):
    email = forms.CharField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={
            "placeholder": "Adres email",
            "class": "form-control",
            "autocomplete": "email"
        })
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Hasło",
            "class": "form-control"
        })
    )


class GiftForm(forms.ModelForm):

    class Meta:
        model = Gift
        fields = ['name', 'description', 'priority', 'approx_price', 'link_to_shop', 'category']

    def clean_approx_price(self):
        price = self.cleaned_data['approx_price']
        if price > 2147483646:
            raise forms.ValidationError("Cena nie może przekraczać 2147483646!")
        return price
