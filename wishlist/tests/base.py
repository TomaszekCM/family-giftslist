from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="test1.test1@test.test",
            email="test1.test1@test.test",
            password="1Qwertyuiop"
        )

    def login_test_user(self):
        self.client.login(username="test1.test1@test.test", password="1Qwertyuiop")

    def get_with_login(self, url_name, *args, **kwargs):
        self.login_test_user()
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))

    def post_with_login(self, url_name, data=None, *args, **kwargs):
        self.login_test_user()
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data or {})
