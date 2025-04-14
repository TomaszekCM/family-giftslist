from django.core.management.base import BaseCommand
from wishlist.models import UserExt
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Command to create new (usually first) user'

    def add_arguments(self, parser):
        parser.add_argument('first_name', type=str, help='Podaj imię użytkownika')
        parser.add_argument('last_name', type=str, help='Podaj nazwisko użytkownika')
        parser.add_argument('dob', type=str, help='Podaj datę urodzenia użytkownika w formacie: "dd.mm.rrrr"')
        parser.add_argument('email', type=str, help='Podaj adres email użytkownika')
        parser.add_argument('password', type=str, help='Podaj hasło')
        parser.add_argument('--admin', action='store_true', help="Czy użytkownik jest administratorem?", default=False)

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        validator = EmailValidator()

        # first of all, we need to validate email format
        try:
            validator(email)
        except ValidationError:
            self.stderr.write(self.style.ERROR("Nieprawidłowy adres email."))
            return

        # and we have to validate date format to avoid errors
        try:
            dob = datetime.strptime(kwargs["dob"], "%d.%m.%Y").date()
        except ValueError:
            self.stderr.write(self.style.ERROR("Błędny format daty. Poprawny format to: dd.mm.rrrr (np. 01.01.1990)"))
            return

        user_data = {
            "username": email,
            "first_name": kwargs["first_name"],
            "last_name": kwargs["last_name"],
            "password": kwargs["password"],
        }

        if kwargs["admin"]:
            user = User.objects.create_superuser(**user_data)
        else:
            user = User.objects.create_user(**user_data)

        UserExt.objects.create(user=user, dob=dob)

        self.stdout.write(self.style.SUCCESS(f"Utworzono użytkownika: {user.username}"))
