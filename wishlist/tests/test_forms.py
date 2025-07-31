from django.test import TestCase
from wishlist.forms import *
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginFormTest(TestCase):
    def test_valid_data(self):
        form = LoginForm(data={"email": "test@test.test", "password": "somepassword"})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = LoginForm(data={"email": "", "password": "somepassword"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        
    def test_invalid_email_format(self):
        form = LoginForm(data={"email": "notanemail", "password": "somepassword"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_password(self):
        form = LoginForm(data={"email": "test@test.test", "password": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)


#  Second branch

class GiftFormTest(TestCase):
    def test_valid_form_with_https(self):
        form = GiftForm(data={
            "name": "Form gift",
            "description": "Nice thing",
            "priority": "average",
            "approx_price": 199,
            "link_to_shop": "https://shop.com",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['link_to_shop'], 'https://shop.com')

    def test_valid_form_with_http(self):
        form = GiftForm(data={
            "name": "Form gift",
            "description": "Nice thing",
            "priority": "average",
            "approx_price": 199,
            "link_to_shop": "http://shop.com",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['link_to_shop'], 'http://shop.com')

    def test_valid_form_simple_url(self):
        form = GiftForm(data={
            "name": "Form gift",
            "description": "Nice thing",
            "priority": "average",
            "approx_price": 199,
            "link_to_shop": "shop.com",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['link_to_shop'], 'http://shop.com')

    def test_invalid_price_too_high(self):
        form = GiftForm(data={
            "name": "Too expensive",
            "description": "Luxury item",
            "priority": "high",
            "approx_price": 9999999999,
            "link_to_shop": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("approx_price", form.errors)
        
    def test_invalid_priority_choice(self):
        form = GiftForm(data={
            "name": "Test gift",
            "description": "Test description",
            "priority": "invalid_priority",
            "approx_price": 100,
            "link_to_shop": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)
        
    def test_negative_price(self):
        form = GiftForm(data={
            "name": "Negative price",
            "description": "Test description",
            "priority": "low",
            "approx_price": -100,
            "link_to_shop": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("approx_price", form.errors)
        
    def test_invalid_url_no_domain(self):
        form = GiftForm(data={
            "name": "Bad URL",
            "description": "Test description",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "not-a-valid-url",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("link_to_shop", form.errors)
        
    def test_invalid_protocol_format(self):
        form = GiftForm(data={
            "name": "Bad Protocol",
            "description": "Test description",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "httpppp//wp.pl",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("link_to_shop", form.errors)
        self.assertIn("protokołu", form.errors["link_to_shop"][0])
        
    def test_url_with_spaces(self):
        form = GiftForm(data={
            "name": "Bad URL",
            "description": "Test description",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "shop com",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("link_to_shop", form.errors)
        
    def test_url_with_invalid_chars(self):
        form = GiftForm(data={
            "name": "Bad URL",
            "description": "Test description",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": 'shop.com"bad',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("link_to_shop", form.errors)
        
    def test_empty_name(self):
        form = GiftForm(data={
            "name": "",
            "description": "Test description",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

class UserDataFormTest(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='Password123'
        )

    def test_valid_data(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "Test description",
            "email": "test@example.com"
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name_day"], {"day": 15, "month": 7})
        self.assertEqual(form.cleaned_data["birth_date"], {"day": 21, "month": 3})

    def test_valid_data_empty_description(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_invalid_month_names_day(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "13",  # Invalid month
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name_day", form.errors)

    def test_invalid_day_names_day(self):
        form = UserDataForm(data={
            "name_day_0": "32",  # Invalid day
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name_day", form.errors)

    def test_invalid_month_dob(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "0",  # Invalid month
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)

    def test_invalid_day_dob(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "32",  # Invalid day
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)

    def test_invalid_date_combination_names_day(self):
        form = UserDataForm(data={
            "name_day_0": "30",  # February never has 30 days
            "name_day_1": "2",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name_day", form.errors)

    def test_invalid_date_combination_dob(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "31",  # April has 30 days
            "birth_date_1": "4",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)

    def test_non_numeric_values(self):
        form = UserDataForm(data={
            "name_day_0": "abc",  # Non-numeric value
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name_day", form.errors)

    def test_missing_required_fields(self):
        form = UserDataForm(data={
            "name_day_1": "7",
            "birth_date_0": "21",
            "birth_date_1": "3",
            "description": "",
            "email": "test@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name_day", form.errors)

    def test_such_an_email_already_exists(self):
        form = UserDataForm(data={
            "name_day_0": "15",
            "name_day_1": "7",
            "birth_date_0": "14",  # Invalid day
            "birth_date_1": "3",
            "description": "",
            "email": "existing@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Użytkownik o takim adresie email już istnieje w systemie.", form.errors['email'])


class AddUserFormTest(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='Password123'
        )

    def test_invalid_password(self):    
        form = UserForm(data={
          "password1": "ABC",
          "password2": "DEF",
          "email": "new.email@email.com",
          "first_name": "Andrzej",
          "last_name": "Andrzejewski",
          "is_superuser": True
          })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('Hasła nie są identyczne.', form.errors['password2'])

    def test_valid_user_form_creation(self):
        data = {
            'email': 'new.user@example.com',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        # Check whether such an user is in the DB
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.email, 'new.user@example.com')
        self.assertEqual(user.username, 'new.user@example.com')
        self.assertEqual(user.first_name, 'Jan')
        self.assertEqual(user.last_name, 'Kowalski')
        self.assertTrue(user.check_password('StrongPassword123'))
        self.assertFalse(user.is_superuser)

        # Check, whether UserExt is created
        self.assertTrue(hasattr(user, 'userext'))
        self.assertIsNotNone(user.userext.pk)

    def test_valid_user_form_creation_superuser(self):
        data = {
            'email': 'admin.user@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password1': 'AdminPassword123',
            'password2': 'AdminPassword123',
            'is_superuser': True,
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_superuser)

    def test_missing_required_fields(self):
        data = {
            'email': '',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'password1': 'password',
            'password2': 'password',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertIn('email', form.errors)
        self.assertIn('This field is required.', form.errors['email'])
        
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserExt.objects.count(), 0)

    def test_invalid_email_format(self):
        data = {
            'email': 'invalid-email',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'password1': 'password',
            'password2': 'password',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_duplicate_email(self):
        data = {
            'email': self.existing_user.email,
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'password1': 'password',
            'password2': 'password',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Użytkownik z tym adresem email już istnieje.', form.errors['email'])

    def test_mismatched_passwords(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'password1': 'password1',
            'password2': 'password2',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('Hasła nie są identyczne.', form.errors['password2'])

    def test_username_set_to_email_on_save(self):
        data = {
            'email': 'user.email@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'user.email@example.com')

    def test_password_is_hashed(self):
        data = {
            'email': 'hashed@example.com',
            'first_name': 'Hashed',
            'last_name': 'Pass',
            'password1': 'MySecretPassword',
            'password2': 'MySecretPassword',
            'is_superuser': False,
        }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertFalse(user.password == 'MySecretPassword')
        self.assertTrue(user.check_password('MySecretPassword'))
        