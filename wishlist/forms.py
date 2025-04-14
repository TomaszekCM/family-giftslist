from django import forms


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
