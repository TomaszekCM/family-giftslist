from django import forms
from wishlist.models import *
from django.contrib.auth.models import User
import re
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import UserExt


class MonthDayInput(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '31',
                'style': 'width: 70px; text-align: center;',
                'aria-label': 'Dzień',
                'placeholder': 'DD'
            }),
            forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '12',
                'style': 'width: 70px; text-align: center;',
                'aria-label': 'Miesiąc',
                'placeholder': 'MM'
            })
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value['day'], value['month']]
        return [None, None]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        for i, subwidget in enumerate(context['widget']['subwidgets']):
            subwidget['template_name'] = 'widgets/monthday_input.html'
            subwidget['field_type'] = 'Dzień' if i == 0 else 'Miesiąc'
        return context

    def format_output(self, rendered_widgets):
        return '<div class="d-flex align-items-start gap-3">' + ''.join(rendered_widgets) + '</div>'


class MonthDayFormField(forms.MultiValueField):
    widget = MonthDayInput

    def __init__(self, **kwargs):
        fields = (
            forms.IntegerField(
                validators=[MinValueValidator(1), MaxValueValidator(31)],
                error_messages={'invalid': 'Wprowadź poprawny dzień (1-31)'}
            ),
            forms.IntegerField(
                validators=[MinValueValidator(1), MaxValueValidator(12)],
                error_messages={'invalid': 'Wprowadź poprawny miesiąc (1-12)'}
            )
        )
        super().__init__(fields, require_all_fields=True, **kwargs)

    def compress(self, data_list):
        if data_list:
            day, month = data_list
            return {'day': day, 'month': month}
        return None

    def clean(self, value):
        # First, perform standard validation
        cleaned_data = super().clean(value)
        if cleaned_data is None:
            return None

        day = cleaned_data.get('day')
        month = cleaned_data.get('month')

        if day is None or month is None:
            raise forms.ValidationError('Oba pola są wymagane')

        # Checking number of days in month
        days_in_month = {
            1: 31,  # January
            2: 29,  # February (assuming leap year for greater flexibility)
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31, # October
            11: 30, # November
            12: 31  # December
        }

        if month in days_in_month:
            max_days = days_in_month[month]
            if day > max_days:
                if month == 2:
                    raise forms.ValidationError(f'Luty ma maksymalnie {max_days} dni')
                raise forms.ValidationError(f'Ten miesiąc ma maksymalnie {max_days} dni')

        return cleaned_data


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

# Form for editing logged in user's self data
class UserDataForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Imię",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź imię"
        })
    )
    last_name = forms.CharField(
        label="Nazwisko",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź nazwisko"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź email"
        })
    )
    birth_date = MonthDayFormField(
        label="Data urodzenia",
        required=False
    )
    name_day = MonthDayFormField(
        label="Data imienin",
        required=False
    )
    description = forms.CharField(
        label="Opis",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź opis",
            "rows": 3
        })
    )
    is_superuser = forms.BooleanField(label="Administrator", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Użytkownik o takim adresie email już istnieje w systemie.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


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
                
            domain = url.split('//')[1]
            if '/' in domain:
                domain = domain.split('/')[0]
                
            if '.' not in domain:
                raise forms.ValidationError("Niepoprawny format adresu URL - brak domeny (np. '.pl', '.com')")
                
        return url


class ImportantDateForm(forms.ModelForm):
    date = MonthDayFormField(
        label="Data",
        required=True
    )
    name = forms.CharField(
        label="Nazwa",
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź nazwę"
        })
    )

    class Meta:
        model = ImportantDate
        fields = ['name', 'date']


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, required=True)
    is_superuser = forms.BooleanField(label='Administrator', required=False)
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Użytkownik z tym adresem email już istnieje.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        if commit:
            user.save()
            UserExt.objects.create(
                user=user
            )
        return user


class UserEditForm(forms.Form):
    birth_date = MonthDayFormField(label="Data urodzenia", required=False)
    name_day = MonthDayFormField(label="Data imienin", required=False)
    description = forms.CharField(
        label="Opis",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Wprowadź opis",
            "rows": 3
        })
    )
    is_superuser = forms.BooleanField(label="Administrator", required=False)
    first_name = forms.CharField(label="Imię", max_length=30, required=True)
    last_name = forms.CharField(label="Nazwisko", max_length=150, required=True)


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return password2

