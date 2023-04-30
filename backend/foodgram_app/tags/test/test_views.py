import typing as t

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase
from tags.models import Tags

User = get_user_model()


class UsersURLTests(APITestCase):
    def setUp(self):
        tag1 = Tags.objects.create(
            name="name1",
            slug="slug1",
            color="#E26C2D",
        )
        self.tag_id1 = tag1.id
        tag2 = Tags.objects.create(
            name="name2",
            slug="slug2",
            color="#E26C2D",
        )

    def test_list_tags(self):
        response = self.client.get("/api/tags/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_tag_by_id(self):
        response = self.client.get(f"/api/tags/{self.tag_id1}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for key, value in [
            ("id", self.tag_id1),
            ("name", "name1"),
            ("color", "#E26C2D"),
        ]:
            with self.subTest(
                f"проверим то ли вернули key={key}, value={value}"
            ):
                self.assertTrue(key in data)
                self.assertEqual(value, data[key])

    def test_tag_be_notvalid_id(self):
        id = "-10"
        response = self.client.get(f"/api/tags/{id}/")
        self.assertEqual(response.status_code, 404)
