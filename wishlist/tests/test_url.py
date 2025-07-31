from django.test import TestCase
from django.urls import reverse, resolve
from wishlist.views import *


class TestUrls(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test1.test1@test.test",
            email="test1.test1@test.test",
            password="1Qwertyuiop"
        )
        self.client.login(username=self.user.username, password="1Qwertyuiop")
        
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

    def test_user_data_resolves(self):
        url = reverse('user_data', args=[self.user.id])
        self.assertEqual(resolve(url).func, user_data)

    def test_edit_user_data_resolves(self):
        url = reverse('edit_user_data')
        self.assertEqual(resolve(url).func, edit_user_data)

    def test_get_user_data_form_resolves(self):
        url = reverse('get_user_data_form')
        self.assertEqual(resolve(url).func, get_user_data_form)

    def test_get_important_date_form_resolves(self):
        url = reverse('get_important_date_form')
        self.assertEqual(resolve(url).func, get_important_date_form)

    def test_add_important_date_resolves(self):
        url = reverse('add_important_date')
        self.assertEqual(resolve(url).func, add_important_date)

    def test_edit_important_date_resolves(self):
        url = reverse('edit_important_date', args=[self.user.id])
        self.assertEqual(resolve(url).func, edit_important_date)

    def test_delete_important_date_resolves(self):
        url = reverse('delete_important_date', args=[self.user.id])
        self.assertEqual(resolve(url).func, delete_important_date)

    def test_user_list_resolves(self):
        url = reverse('user_list')
        self.assertEqual(resolve(url).func.view_class, UserListView)

    def test_user_add_ajax_resolves(self):
        url = reverse('user_add_ajax')
        self.assertEqual(resolve(url).func, add_user_ajax)

    def test_edit_user_resolves(self):
        url = reverse('edit_user', args=[self.user.id])
        self.assertEqual(resolve(url).func, edit_user)

    def test_change_password_resolves(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_get_change_password_form_resolves(self):
        url = reverse('get_change_password_form')
        self.assertEqual(resolve(url).func, get_change_password_form)
