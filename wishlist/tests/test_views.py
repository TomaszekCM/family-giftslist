from django.urls import reverse
from wishlist.tests.base import TestBase
from wishlist.models import *
import json


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


class UserDataViewTest(TestBase):
    def setUp(self):
        super().setUp()
        self.user_ext = UserExt.objects.create(
            user=self.user,
            names_day={"month": 6, "day": 15},
            dob={"month": 3, "day": 21},
            description="Original description"
        )

    def test_get_user_data_form(self):
        response = self.get_with_login("get_user_data_form")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/user_data_form.html")
        self.assertContains(response, "Imię")
        self.assertContains(response, "Nazwisko")
        self.assertContains(response, "Email")
        self.assertContains(response, "Data urodzenia")
        self.assertContains(response, "Data imienin")
        
    def test_get_user_data_form_requires_login(self):
        response = self.client.get(reverse("get_user_data_form"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_edit_user_data_valid(self):
        data = {
            "name_day_0": "22",
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Updated description",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        
        # Verify changes
        self.user_ext.refresh_from_db()
        self.assertEqual(self.user_ext.names_day["day"], 22)
        self.assertEqual(self.user_ext.names_day["month"], 7)
        self.assertEqual(self.user_ext.dob["day"], 12)
        self.assertEqual(self.user_ext.dob["month"], 4)
        self.assertEqual(self.user_ext.description, "Updated description")

    def test_edit_user_data_invalid_month(self):
        data = {
            "name_day_0": "15",
            "name_day_1": "13",  # Invalid month
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("name_day", response.json()["errors"])

    def test_edit_user_data_invalid_day(self):
        data = {
            "name_day_0": "32",  # Invalid day
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("name_day", response.json()["errors"])

    def test_edit_user_data_invalid_date_combination(self):
        data = {
            "name_day_0": "30",  # February never has 30 days
            "name_day_1": "2",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("name_day", response.json()["errors"])

    def test_edit_user_data_requires_login(self):
        data = {
            "name_day_0": "22",
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.client.post(reverse("edit_user_data"), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_edit_user_data_invalid_method(self):
        response = self.client.get(reverse("edit_user_data"))
        self.assertEqual(response.status_code, 405)

    def test_edit_user_data_missing_fields(self):
        data = {
            # missing name_day_0
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("name_day", response.json()["errors"])

    def test_edit_user_data_non_numeric_values(self):
        data = {
            "name_day_0": "abc",  # Non-numeric value
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "Test",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("name_day", response.json()["errors"])

    def test_edit_user_data_empty_description(self):
        data = {
            "name_day_0": "22",
            "name_day_1": "7",
            "birth_date_0": "12",
            "birth_date_1": "4",
            "description": "",
            "email": "test1.test1@test.test"
        }
        response = self.post_with_login("edit_user_data", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        
        self.user_ext.refresh_from_db()
        self.assertEqual(self.user_ext.description, "")



# Branch 5 - users list
class UserListViewTest(TestBase):
    def test_user_list_requires_login(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_user_list_renders_for_admin(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.user.username, password="1Qwertyuiop")
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lista użytkowników")


class AddUserAjaxTest(TestBase):
    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.user.username, password="1Qwertyuiop")

    def test_add_user_ajax_get(self):
        response = self.client.get(reverse("user_add_ajax"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Imię")

    def test_add_user_ajax_post_valid(self):
        data = {
            "email": "newuser@test.com",
            "first_name": "Nowy",
            "last_name": "Użytkownik",
            "password1": "NoweHaslo123",
            "password2": "NoweHaslo123",
            "is_superuser": False,
        }
        response = self.client.post(reverse("user_add_ajax"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())

    def test_add_user_ajax_post_invalid(self):
        data = {
            "email": "newuser@test.com",
            "first_name": "",
            "last_name": "",
            "password1": "NoweHaslo123",
            "password2": "zlehaslo",
            "is_superuser": False,
        }
        response = self.client.post(reverse("user_add_ajax"), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("form", response.content.decode())

    def test_add_user_ajax_by_standard_user_rejected(self):
        data = {
            "email": "newuser@test.com",
            "first_name": "Imie",
            "last_name": "Nawzwisko",
            "password1": "NoweHaslo123",
            "password2": "NoweHaslo123",
            "is_superuser": False,
        }
        response = self.post_with_standard_login("user_add_ajax", data)
        self.assertEqual(response.status_code, 403)


class EditUserViewTest(TestBase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user.username, password="1Qwertyuiop")
        self.other_user = User.objects.create_user(
            username="other@test.com",
            email="other@test.com",
            password="1Qwertyuiop",
            first_name="Piotr",
            last_name="Pietrzak"
        )
        self.other_ext = UserExt.objects.create(
            user=self.other_user,
            dob={"month": 2, "day": 28},
            names_day={"month": 3, "day": 3},
            description="Opis"
        )

    def test_get_edit_user_form(self):
        response = self.client.get(reverse("edit_user", args=[self.other_user.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.json()["form_html"])

    def test_edit_user_valid(self):
        data = {
            "first_name": "Piotr7",
            "last_name": "Pietrzak",
            "is_superuser": True,
            "birth_date_0": "31",
            "birth_date_1": "1",
            "name_day_0": "3",
            "name_day_1": "3",
            "description": "Nowy opis"
        }
        response = self.client.post(reverse("edit_user", args=[self.other_user.id]), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.first_name, "Piotr7")
        self.assertTrue(self.other_user.is_superuser)

    def test_edit_user_invalid(self):
        data = {
            "first_name": "",
            "last_name": "",
            "is_superuser": True,
            "birth_date_0": "32",
            "birth_date_1": "1",
            "name_day_0": "3",
            "name_day_1": "3",
            "description": "Nowy opis"
        }
        response = self.client.post(reverse("edit_user", args=[self.other_user.id]), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn("form_html", response.json())


class ChangePasswortViewTest(TestBase):
    
    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.user.username, password="1Qwertyuiop")
        self.change_password_url = reverse('change_password')
        self.get_change_password_form_url = reverse('get_change_password_form')

    def test_get_change_password_form_authenticated(self):
        """
        Check, whether logged in user can get the change password form.
        """
        response = self.client.get(self.get_change_password_form_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/change_password_form.html')
        self.assertContains(response, '<form id="change-password-form" method="post">')
        self.assertContains(response, '<input type="password" name="password1"')
        self.assertContains(response, '<input type="password" name="password2"')

    def test_get_change_password_form_unauthenticated(self):
        """
        Check whether not logged in user is being redirected to login page
        """
        self.client.logout()
        response = self.client.get(self.get_change_password_form_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_change_password_success(self):
        """
        Check correct password change by the logged in user
        """
        new_password = 'newsecurepassword123'
        data = {
            'password1': new_password,
            'password2': new_password,
        }

        response = self.client.post(self.change_password_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        self.client.logout()
        logged_in = self.client.login(username=self.user.username, password=new_password)
        self.assertTrue(logged_in)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
    
    def test_change_password_mismatched_passwords(self):
        """
        Check whether different new passwords generate validation error
        """
        data = {
            'password1': 'newpassword1',
            'password2': 'newpassword2',
        }
        response = self.client.post(self.change_password_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.content)
        self.assertIn('form_html', json_response)
        self.assertIn('Hasła nie są identyczne.', json_response['form_html'])
        self.assertIn('is-invalid', json_response['form_html'])

        self.client.logout()
        logged_in = self.client.login(username=self.user.username, password='newpassword1')
        self.assertFalse(logged_in)

    def test_change_password_empty_password(self):
        """
        Check whether empty passwords generate validation error (required).
        """
        data = {
            'password1': '',
            'password2': '',
        }
        response = self.client.post(self.change_password_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.content)
        self.assertIn('form_html', json_response)


    def test_change_password_unauthenticated(self):
        """
        Check whether not logged in user can reach password change
        """
        self.client.logout()
        data = {
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(self.change_password_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_change_password_get_request(self):
        """
        Checks if a GET request to change_password returns 405 Method Not Allowed. 
        """
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 405)
        
