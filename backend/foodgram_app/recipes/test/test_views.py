import typing as t

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token

User = get_user_model()


class UsersURLTests(APITestCase):
    def __registration_user(self):
        user_data = {
            "username": "username",
            "email": "foobar@example.com",
            "password": "pass11",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        response = self.client.post("/api/users/", user_data, format="json")
        self.assertEqual(response.status_code, 201)

    def __login_user(self):
        login_data = {
            "email": "foobar@example.com",
            "password": "pass11",
        }
        response = self.client.post(
            "/api/auth/token/login/", login_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("auth_token" in response.json())
        return response.json().get("auth_token")

    def create_authorized_client(self):
        self.authorized_client = APIClient()
        self.__registration_user()
        token_user = self.__login_user()
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION="Token " + token_user
        )

    def setUp(self):
        self.guest_client = APIClient()
        self.create_authorized_client()
        self.all_clients = [self.guest_client, self.authorized_client]

    def test_status_code_list_recipes(self):
        response = None
        for client in self.all_clients:
            response = client.get("/api/recipes/")
            self.assertEqual(response.status_code, 200)
        return response

    def __crete_recipe(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile(
            "small.gif", small_gif, content_type="image/gif"
        )
        data_reciepe = {
            "image": uploaded,
            "name": "test_name",
            "text": "10" * 100,
            "cooking_time": 20,
        }
        response = self.authorized_client.post(
            "/api/recipes/", data=data_reciepe
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        for key, type_value in [
            ("id", int),
            ("author", dict),
            ("image", str),
            ("cooking_time", int),
        ]:
            with self.subTest(f"key={key}; type={type_value}"):
                self.assertTrue(key in data)
                value = data.get(key)
                self.assertTrue(isinstance(value, type_value))

        with self.subTest("check author format"):
            for key, type_value in [
                ("id", int),
                ("username", str),
                ("email", str),
                ("first_name", str),
                ("last_name", str),
            ]:
                with self.subTest(f"key={key}; type={type_value}"):
                    self.assertTrue(key in data["author"])
                    value = data["author"].get(key)
                    self.assertTrue(isinstance(value, type_value))
        return response

    def test_auth_user_create_recipe(self):
        self.__crete_recipe()

    def test_notauth_user_create_recipe(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile(
            "small.gif", small_gif, content_type="image/gif"
        )
        data_reciepe = {
            "image": uploaded,
            "name": "test_name",
            "text": "10" * 100,
            "cooking_time": 20,
        }
        response = self.guest_client.post("/api/recipes/", data=data_reciepe)
        self.assertNotEqual(response.status_code, 201)

    def test_list_recipe(self):
        response1 = self.test_status_code_list_recipes()
        items1 = response1.json()
        self.__crete_recipe()
        response2 = self.test_status_code_list_recipes()
        items2 = response2.json()
        self.assertEqual(len(items1) + 1, len(items2))

    def test_recipe_by_id(self, id=None):
        if not id:
            response = self.__crete_recipe()
            data = response.json()
            id = data.get("id")
        response = self.client.get(f"/api/recipes/{id}/")
        self.assertEqual(response.status_code, 200)
        return response

    def test_update_recipe_by_id(self):
        response = self.__crete_recipe()
        data = response.json()
        id = data.get("id")
        response = self.client.patch(
            f"/api/recipes/{id}/", data={"text": "new_text"}
        )
        self.assertEqual(response.status_code, 401)

        response = self.authorized_client.patch(
            f"/api/recipes/{id}/", data={"text": "new_text"}
        )
        self.assertEqual(response.json().get("text"), "new_text")
        self.assertEqual(response.status_code, 200)
        response = self.test_recipe_by_id(id)
        self.assertEqual(response.json().get("text"), "new_text")
        # TODO нельзя менять чужие посты !!
        # TODO проверить формат выхода

    def test_delete_recipe_by_id(self):
        response = self.__crete_recipe()
        data = response.json()
        id = data.get("id")
        response = self.client.delete(
            f"/api/recipes/{id}/",
        )
        self.assertEqual(response.status_code, 401)
        response = self.authorized_client.delete(
            f"/api/recipes/{id}/",
        )
        self.assertEqual(response.status_code, 204)
        response = self.authorized_client.get(f"/api/recipes/{id}/")
        self.assertEqual(response.status_code, 404)
