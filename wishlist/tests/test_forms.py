from django.test import TestCase
from wishlist.forms import *


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
