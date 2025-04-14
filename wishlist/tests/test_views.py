from django.urls import reverse
from wishlist.tests.base import TestBase


class LoginViewTest(TestBase):
    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "email": "test1.test1@test.test",
            "password": "1Qwertyuiop"
        })
        self.assertRedirects(response, reverse("home"))


class LandingPageTest(TestBase):
    def test_landing_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Witaj na stronie, gdzie możesz tworzyć i przeglądać listy prezentów dla bliskich!")
