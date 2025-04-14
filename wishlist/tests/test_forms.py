from django.test import TestCase
from wishlist.forms import LoginForm


class LoginFormTest(TestCase):
    def test_valid_data(self):
        form = LoginForm(data={"email": "test@test.test", "password": "somepassword"})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = LoginForm(data={"email": "", "password": "somepassword"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
