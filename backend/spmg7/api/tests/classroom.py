from django.test import TestCase, Client
from rest_framework import status
from datetime import date
from django.urls import reverse
from ..models import Classroom, Profile
import json

client = Client()


class GetClassById(TestCase):
    def setUp(self):
        self.classroom = Classroom.objects.create(
            class_name="g99", course_id=1, start_datetime=date.today(),
            end_datetime=date.today(),
            trainer_id=None, enroll_start=date.today(),
            enroll_end=date.today(),
            class_size=30)

    def tearDown(self):
        self.classroom = None

    def test_valid_classroom(self):
        response = client.get(reverse("get_class_by_id", kwargs={
            "classroom_id": self.classroom.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data))[0]["id"], self.classroom.id)

    def test_invalid_classroom(self):
        response = client.get(reverse("get_class_by_id", kwargs={
            "classroom_id": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetCourseTaughtByTrainer(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(username="testuser1", display_name="Test User 1", is_admin=0)
        self.classroom = Classroom.objects.create(
            class_name="g99", course_id=1, start_datetime=date.today(),
            end_datetime=date.today(),
            trainer_id=self.profile.pk, enroll_start=date.today(),
            enroll_end=date.today(),
            class_size=30)

    def tearDown(self):
        self.profile = None
        self.classroom = None

    def test_valid_course_taught_by_trainer(self):
        response = client.get(reverse("get_course_of_trainer", kwargs={
            "username": self.profile.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data))[0]["id"], self.classroom.id)

    def test_not_a_trainer(self):
        response = client.get(reverse("get_course_of_trainer", kwargs={
            "username": "testuser2"}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetClassesTaughtByTrainer(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(username="testuser1", display_name="Test User 1", is_admin=0)

        self.classroom = Classroom.objects.create(
            class_name="g99", course_id=1, start_datetime=date.today(),
            end_datetime=date.today(),
            trainer_id=self.profile.pk, enroll_start=date.today(),
            enroll_end=date.today(),
            class_size=30)

    def tearDown(self):
        self.profile = None
        self.classroom = None

    def test_valid_classes_taught_by_trainer(self):
        response = client.get(reverse("get_classes_of_trainer", kwargs={
            "username": self.profile.pk, "course_id": self.classroom.course_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(json.dumps(response.data))[0]["id"], self.classroom.id)

    def test_invalid_classes_taught_by_trainer(self):
        response = client.get(reverse("get_classes_of_trainer", kwargs={
            "username": "testuser2", "course_id": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
