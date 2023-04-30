import typing as t

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ingredients.models import Ingredients
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from tags.models import Tags

User = get_user_model()


class UsersURLTests(APITestCase):
    def __registration_user(self, user_data):
        response = self.client.post("/api/users/", user_data, format="json")
        self.assertEqual(response.status_code, 201)

    def __login_user(self, login_data):
        response = self.client.post(
            "/api/auth/token/login/", login_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("auth_token" in response.json())
        return response.json().get("auth_token")

    def create_authorized_client(self, client, user_data):
        self.__registration_user(user_data)
        login_data = {
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        }

        token_user = self.__login_user(login_data)
        client.credentials(HTTP_AUTHORIZATION="Token " + token_user)

    def create_authorized_clients(self):
        self.authorized_client_athor = APIClient()
        user_data_author = {
            "username": "username",
            "email": "foobar@example.com",
            "password": "pass11",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        self.create_authorized_client(
            self.authorized_client_athor, user_data_author
        )
        self.authorized_client_noauthor = APIClient()
        user_data_notauthor = {
            "username": "username2",
            "email": "noauthor@example.com",
            "password": "pass11",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        self.create_authorized_client(
            self.authorized_client_noauthor, user_data_notauthor
        )

    def create_tags(self):
        self.tag1 = Tags.objects.create(
            name="name1", color="#E26C2D", slug="slug1"
        )
        self.tag2 = Tags.objects.create(
            name="name2", color="#E26C2D", slug="slug2"
        )

    def create_ingredients(self):
        self.ingredient1 = Ingredients.objects.create(
            name="name1", measurement_unit="measurement_unit1"
        )
        self.ingredient2 = Ingredients.objects.create(
            name="name2", measurement_unit="measurement_unit2"
        )

    def setUp(self):
        self.guest_client = APIClient()
        self.create_authorized_clients()
        self.all_clients = [
            self.guest_client,
            self.authorized_client_athor,
            self.authorized_client_noauthor,
        ]
        self.create_tags()
        self.create_ingredients()

    # def test_status_code_list_recipes(self):
    #     response = None
    #     for client in self.all_clients:
    #         response = client.get("/api/recipes/")
    #         self.assertEqual(response.status_code, 200)
    #         for item_recipe in response.json():
    #             self.__check_foramt_recipe(item_recipe, flag_read=True)
    #     return response

    def __check_format_recipe_main(self, data):
        for key, type_value in [
            ("id", int),
            ("author", dict),
            ("image", str),
            ("cooking_time", int),
            ("tags", list),
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

    def __check_foramt_recipe(self, data, flag_read=False):
        self.__check_format_recipe_main(data)
        self.assertEqual(len(data.get("tags")), 2)
        with self.subTest("check tags format"):
            for tag_info in data["tags"]:
                if not flag_read:
                    self.assertTrue(isinstance(tag_info, int))
                else:
                    for key, type_value in [
                        ("id", int),
                        ("name", str),
                        ("color", str),
                        ("slug", str),
                    ]:
                        self.assertTrue(key in tag_info)
                        value = tag_info.get(key)
                        self.assertTrue(isinstance(value, type_value))

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
            "tags": [self.tag1.id, self.tag2.id],
            "ingredients": [
                {
                    "id": 1,
                    "amount": 1,
                }
            ],
        }
        print(data_reciepe)
        response = self.authorized_client_athor.post(
            "/api/recipes/", data=data_reciepe
        )
        print(response.json())
        exit()
        self.assertEqual(response.status_code, 201)
        self.__check_foramt_recipe(response.json())

        return response

    def test_auth_user_create_recipe(self):
        self.__crete_recipe()

    # def test_notauth_user_create_recipe(self):
    #     small_gif = (
    #         b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    #         b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    #         b"\x02\x4c\x01\x00\x3b"
    #     )
    #     uploaded = SimpleUploadedFile(
    #         "small.gif", small_gif, content_type="image/gif"
    #     )
    #     data_reciepe = {
    #         "image": uploaded,
    #         "name": "test_name",
    #         "text": "10" * 100,
    #         "cooking_time": 20,
    #     }
    #     response = self.guest_client.post("/api/recipes/", data=data_reciepe)
    #     self.assertNotEqual(response.status_code, 201)

    # def test_list_recipe(self):
    #     response1 = self.test_status_code_list_recipes()
    #     items1 = response1.json()
    #     self.__crete_recipe()
    #     response2 = self.test_status_code_list_recipes()
    #     items2 = response2.json()
    #     self.assertEqual(len(items1) + 1, len(items2))

    # def test_recipe_by_id(self, id=None):
    #     if not id:
    #         response = self.__crete_recipe()
    #         data = response.json()
    #         id = data.get("id")
    #     response = self.client.get(f"/api/recipes/{id}/")
    #     self.assertEqual(response.status_code, 200)
    #     self.__check_foramt_recipe(response.json(), flag_read=True)

    #     return response

    # def test_update_recipe_by_id(self):
    #     response = self.__crete_recipe()
    #     data = response.json()
    #     id = data.get("id")
    #     with self.subTest(f"Чтобы изменить рецепт нужно авторизоваться!"):
    #         response = self.client.patch(
    #             f"/api/recipes/{id}/", data={"text": "new_text"}
    #         )
    #         self.assertEqual(response.status_code, 401)
    #     with self.subTest(f"Автор может менять рецепт!"):
    #         response = self.authorized_client_athor.patch(
    #             f"/api/recipes/{id}/", data={"text": "new_text"}
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(response.json().get("text"), "new_text")
    #         self.__check_foramt_recipe(response.json(), flag_read=False)

    #         response = self.test_recipe_by_id(id)
    #         self.assertEqual(response.json().get("text"), "new_text")

    #     with self.subTest("Дргой пользователь не может поменять мой рецепт"):
    #         response = self.authorized_client_noauthor.patch(
    #             f"/api/recipes/{id}/", data={"text": "new_text"}
    #         )
    #         self.assertEqual(response.status_code, 403)

    # def test_delete_recipe_by_id(self):
    #     with self.subTest("Корректный сценарий удаления рецепта"):
    #         response = self.__crete_recipe()
    #         data = response.json()
    #         id = data.get("id")
    #         with self.subTest("Нужно авторизоваться!"):
    #             response = self.client.delete(
    #                 f"/api/recipes/{id}/",
    #             )
    #             self.assertEqual(response.status_code, 401)
    #         response = self.authorized_client_athor.delete(
    #             f"/api/recipes/{id}/",
    #         )
    #         self.assertEqual(response.status_code, 204)
    #         response = self.authorized_client_athor.get(f"/api/recipes/{id}/")
    #         self.assertEqual(response.status_code, 404)
    #     with self.subTest("Друой пользователь не может удалить рецепт автора"):
    #         response = self.__crete_recipe()
    #         data = response.json()
    #         id = data.get("id")
    #         response = self.authorized_client_noauthor.delete(
    #             f"/api/recipes/{id}/",
    #         )
    #         self.assertEqual(response.status_code, 403)
