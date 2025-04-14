from django.test import SimpleTestCase
from django.urls import reverse, resolve
from wishlist.views import LoginView, LandingPage


class TestUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, LandingPage)
