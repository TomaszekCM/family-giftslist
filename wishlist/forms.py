from django import forms
from wishlist.models import *
import re


class LoginForm(forms.Form):
    email = forms.EmailField(
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

    def clean_link_to_shop(self):
        url = self.cleaned_data.get('link_to_shop')
        if url:
            # Delete white spaces from start and end of the url
            url = url.strip()
            
            # Check if the url contains forbidden characters
            if re.search(r'[<>"\']', url):
                raise forms.ValidationError("URL zawiera niedozwolone znaki")
                
            # Check if the url contains spaces
            if ' ' in url:
                raise forms.ValidationError("URL nie może zawierać spacji")
            
            # If the url tries to use a protocol, but does it incorrectly
            if re.match(r'^(?!https?://).*?//', url):
                raise forms.ValidationError("Niepoprawny format protokołu - adres powinien zaczynać się od 'http://' lub 'https://' lub nie zawierać '//' wcale")
                
            # If there is no protocol, add http://
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
                
            # Check if the url contains at least one dot in the domain part
            domain = url.split('//')[1]
            if '/' in domain:
                domain = domain.split('/')[0]
                
            if '.' not in domain:
                raise forms.ValidationError("Niepoprawny format adresu URL - brak domeny (np. '.pl', '.com')")
                
        return url
