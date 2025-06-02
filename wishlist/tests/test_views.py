from django.urls import reverse
from wishlist.tests.base import TestBase
from wishlist.models import *


class LoginViewTest(TestBase):
    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "email": "test1.test1@test.test",
            "password": "1Qwertyuiop"
        })
        self.assertRedirects(response, reverse("home"))
        
    def test_login_wrong_password(self):
        response = self.client.post(reverse("login"), {
            "email": "test1.test1@test.test",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zły email lub hasło")
        
    def test_login_nonexistent_user(self):
        response = self.client.post(reverse("login"), {
            "email": "nonexistent@test.test",
            "password": "somepassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zły email lub hasło")
        
    def test_already_logged_in_redirect(self):
        self.client.login(username="test1.test1@test.test", password="1Qwertyuiop")
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("home"))


class LandingPageTest(TestBase):
    def test_landing_page_loads(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Witaj na stronie, gdzie możesz tworzyć i przeglądać listy prezentów dla bliskich!")
        
    def test_landing_redirects_when_logged_in(self):
        self.client.login(username="test1.test1@test.test", password="1Qwertyuiop")
        response = self.client.get(reverse("landing"))
        self.assertRedirects(response, reverse("home"))


# Second branch

class HomePageTest(TestBase):
    def test_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_home_renders_for_logged_in_user(self):
        response = self.get_with_login("home")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIn("form", response.context)
        
    def test_home_shows_user_gifts(self):
        self.client.login(username="test1.test1@test.test", password="1Qwertyuiop")
        Gift.objects.create(
            name="Test Gift",
            description="Test Description",
            priority="high",
            approx_price=100,
            who_wants_it=self.user
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Test Gift")
        
    def test_home_doesnt_show_others_gifts(self):
        other_user = User.objects.create_user(
            username="other@test.com",
            email="other@test.com",
            password="1Qwertyuiop"
        )
        Gift.objects.create(
            name="Other's Gift",
            description="Not yours",
            priority="high",
            approx_price=100,
            who_wants_it=other_user
        )
        response = self.get_with_login("home")
        self.assertNotContains(response, "Other's Gift")


class AddGiftViewTest(TestBase):
    def test_add_gift_valid_data(self):
        data = {
            "name": "Test Present",
            "description": "Cool gift",
            "priority": "average",
            "approx_price": 150,
            "link_to_shop": "https://example.com",
        }
        response = self.post_with_login("add_gift", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Gift.objects.filter(name="Test Present").exists())

    def test_add_gift_invalid_data(self):
        data = {
            "name": "",
            "description": "Missing name",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "",
        }
        response = self.post_with_login("add_gift", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())
        self.assertEqual(Gift.objects.count(), 0)
        
    def test_add_gift_requires_login(self):
        data = {
            "name": "Test Present",
            "description": "Cool gift",
            "priority": "average",
            "approx_price": 150,
        }
        response = self.client.post(reverse("add_gift"), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        
    def test_add_gift_invalid_method(self):
        response = self.client.get(reverse("add_gift"))
        self.assertEqual(response.status_code, 405)


class DeleteGiftViewTest(TestBase):
    def setUp(self):
        super().setUp()
        self.gift = Gift.objects.create(
            name="Gift to delete",
            description="To be removed",
            priority="low",
            approx_price=100,
            link_to_shop="https://shop.com",
            who_wants_it=self.user
        )

    def test_delete_own_gift(self):
        response = self.post_with_login("delete_gift", {"gift_id": self.gift.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Gift.objects.filter(id=self.gift.id).exists())

    def test_cannot_delete_other_users_gift(self):
        other_user = User.objects.create_user(
            username="someone", email="someone@test.com", password="Pass1234"
        )
        other_gift = Gift.objects.create(
            name="Other gift",
            description="Not yours",
            priority="high",
            approx_price=50,
            link_to_shop="",
            who_wants_it=other_user
        )
        response = self.post_with_login("delete_gift", {"gift_id": other_gift.id})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Gift.objects.filter(id=other_gift.id).exists())
        
    def test_delete_nonexistent_gift(self):
        response = self.post_with_login("delete_gift", {"gift_id": 99999})
        self.assertEqual(response.status_code, 400)
        
    def test_delete_gift_requires_login(self):
        response = self.client.post(reverse("delete_gift"), {"gift_id": self.gift.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        self.assertTrue(Gift.objects.filter(id=self.gift.id).exists())
        
    def test_delete_gift_invalid_method(self):
        response = self.client.get(reverse("delete_gift"))
        self.assertEqual(response.status_code, 405)


class EditGiftViewTest(TestBase):
    def setUp(self):
        super().setUp()
        self.gift = Gift.objects.create(
            name="Original Name",
            description="Edit me",
            priority="average",
            approx_price=200,
            link_to_shop="https://example.com",
            who_wants_it=self.user
        )

    def test_edit_gift_valid(self):
        data = {
            "gift_id": self.gift.id,
            "name": "Updated Name",
            "description": "Now better",
            "priority": "average",
            "approx_price": 300,
            "link_to_shop": "https://example.com/new",
        }
        response = self.post_with_login("edit_gift", data)
        self.assertEqual(response.status_code, 200)

        self.gift.refresh_from_db()
        self.assertEqual(self.gift.name, "Updated Name")
        self.assertEqual(self.gift.priority, "average")

    def test_edit_invalid_data(self):
        data = {
            "gift_id": self.gift.id,
            "name": "",
            "description": "Missing name",
            "priority": "low",
            "approx_price": 100,
            "link_to_shop": "",
        }
        response = self.post_with_login("edit_gift", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())
        
    def test_edit_nonexistent_gift(self):
        data = {
            "gift_id": 99999,
            "name": "Updated Name",
            "description": "Now better",
            "priority": "average",
            "approx_price": 300,
        }
        response = self.post_with_login("edit_gift", data)
        self.assertEqual(response.status_code, 404)
        
    def test_edit_other_users_gift(self):
        other_user = User.objects.create_user(
            username="other@test.com",
            email="other@test.com",
            password="1Qwertyuiop"
        )
        other_gift = Gift.objects.create(
            name="Other's Gift",
            description="Not yours",
            priority="high",
            approx_price=100,
            who_wants_it=other_user
        )
        data = {
            "gift_id": other_gift.id,
            "name": "Trying to change",
            "description": "Should not work",
            "priority": "low",
            "approx_price": 50,
        }
        response = self.post_with_login("edit_gift", data)
        self.assertEqual(response.status_code, 404)
        other_gift.refresh_from_db()
        self.assertEqual(other_gift.name, "Other's Gift")
        
    def test_edit_gift_requires_login(self):
        data = {
            "gift_id": self.gift.id,
            "name": "Updated Name",
            "description": "Now better",
            "priority": "average",
            "approx_price": 300,
        }
        response = self.client.post(reverse("edit_gift"), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
        
    def test_edit_gift_invalid_method(self):
        response = self.client.get(reverse("edit_gift"))
        self.assertEqual(response.status_code, 405)
