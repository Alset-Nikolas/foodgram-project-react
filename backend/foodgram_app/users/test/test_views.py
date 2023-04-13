import typing as t

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersURLTests(TestCase):
    ALL_REG_USERS = 1

    def create_authorized_client(self):
        self.authorized_client = Client()
        self.authorized_client_password = "!"
        self.authorized_client_username = "username"
        self.authorized_client_email = "email@mail.ru"
        self.auth_user = User.objects.create_user(
            username=self.authorized_client_username,
            password=self.authorized_client_password,
            email=self.authorized_client_email,
        )
        self.authorized_client.force_login(self.auth_user)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = None
        self.authorized_client_password = None
        self.auth_user = None
        self.create_authorized_client()
        self.all_clients = [self.guest_client, self.authorized_client]

    def __check_format_response_users(self, users):
        for user_info in users:
            with self.subTest(
                f'check user info response, name_user: {user_info.get("username", "ERROR_NAME!")}'
            ):
                for key_name, type_name in [
                    ("id", int),
                    ("username", str),
                    ("email", str),
                    ("last_name", str),
                    ("first_name", str),
                ]:
                    with self.subTest(
                        f"key:{key_name}; type_name: {type_name}; user_info: {user_info.get(key_name, None)}"
                    ):
                        self.assertTrue(
                            isinstance(
                                user_info.get(key_name, None), type_name
                            )
                        )

    def test_status_code_list_users(self, len_users=1):
        for clint in self.all_clients:
            response = clint.get("/api/users/")
            users_list: t.List[t.Dict] = response.json()
            self.__check_format_response_users(users_list)
            self.assertEqual(response.status_code, 200)
            with self.subTest(f"check q users"):
                self.assertTrue(len(users_list), len_users)

    def test_valid_token_user(self):
        response = self.authorized_client.post(
            "/api/auth/token/login/",
            data={
                "password": self.authorized_client_password,
                "email": self.authorized_client_email,
            },
        )
        data = response.json()
        self.assertTrue(isinstance(data.get("auth_token"), str))
        self.assertEqual(response.status_code, 200)
        return data.get("auth_token")

    def test_valid_logout_user(self):
        token_user = self.test_valid_token_user()
        response = self.client.post(
            "/api/auth/token/logout/",
            headers={"Authorization": f"Token {token_user}"},
        )
        self.assertEqual(response.status_code, 204)
        token_user2 = self.test_valid_token_user()
        self.assertNotEqual(token_user, token_user2)
        self.authorized_client.force_login(self.auth_user)

    def __registration_user(self):
        UsersURLTests.ALL_REG_USERS += 1
        id = UsersURLTests.ALL_REG_USERS
        reg_user_name = f"test_user{id}"
        reg_user_email = f"test_user{id}_email@mail.com"
        reg_user_first_name = f"test_user{id}_first_name"
        reg_user_last_name = f"test_user{id}_last_name"

        response = self.client.post(
            "/api/users/",
            data={
                "username": reg_user_name,
                "email": reg_user_email,
                "first_name": reg_user_first_name,
                "last_name": reg_user_last_name,
                "password": "!",
            },
        )
        return response

    def test_valid_registration_user(self):
        response_registration_user_1 = self.__registration_user()
        self.assertEqual(response_registration_user_1.status_code, 201)
        self.test_status_code_list_users(UsersURLTests.ALL_REG_USERS)

    def test_valid_change_password(self):
        response = self.authorized_client.post(
            "/api/auth/token/login/",
            data={
                "password": self.authorized_client_password,
                "email": self.authorized_client_email,
            },
        )
        token_user = response.json().get("auth_token")

        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/api/users/set_password/",
            headers={"Authorization": f"Token {token_user}"},
            data={
                "current_password": self.authorized_client_password,
                "new_password": "qwert1235QWER!@#$",
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.authorized_client.post(
            "/api/auth/token/login/",
            data={
                "password": self.authorized_client_password,
                "email": self.authorized_client_email,
            },
        )
        self.assertEqual(response.status_code, 400)
