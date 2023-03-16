from django.test import TestCase, Client
from ..serializers import ProfileSerializer
from ..views import Profile
from django.urls import reverse
from ..models import Profile
from rest_framework import serializers, status
import json

client = Client()


class GetUserByUsername(TestCase):
    def setUp(self):
        self.user = Profile.objects.create(username="validuser1", display_name="Valid User 1", is_admin=False)

    def tearDown(self):
        self.user = None

    def test_valid_user(self):
        response = client.get(reverse("get_user_by_username", kwargs={"username": self.user.pk}))
        serializer = ProfileSerializer(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data))[0], serializer.data)

    def test_invalid_user(self):
        response = client.get(reverse("get_user_by_username", kwargs={"username": "invaliduser1"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
