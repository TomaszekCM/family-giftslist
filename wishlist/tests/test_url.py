from django.test import SimpleTestCase
from django.urls import reverse, resolve
from wishlist.views import LoginView, LandingPage, HomePage, logout_view, add_gift, delete_gift, edit_gift


class TestUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_landing_url_resolves(self):
        url = reverse('landing')
        self.assertEqual(resolve(url).func.view_class, LandingPage)
        
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomePage)
        
    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)
        
    def test_add_gift_url_resolves(self):
        url = reverse('add_gift')
        self.assertEqual(resolve(url).func, add_gift)
        
    def test_delete_gift_url_resolves(self):
        url = reverse('delete_gift')
        self.assertEqual(resolve(url).func, delete_gift)
        
    def test_edit_gift_url_resolves(self):
        url = reverse('edit_gift')
        self.assertEqual(resolve(url).func, edit_gift)
