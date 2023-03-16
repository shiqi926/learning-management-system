from django.test import TestCase, Client
from rest_framework import status
from datetime import date
from ..serializers import ChapterSerializer
from ..views import Chapter
from django.urls import reverse
from ..models import Chapter, Classroom, Course, Profile, Progress
import json

client = Client()


class GetChapterInClassTest(TestCase):
    def setUp(self):
        materials = {
            "0": {
                "url": "s3.bucket.fake.com",
                "type": "pdf",
                "title": "Sample Material"
            },
            "1": {
                "url": "s3.bucket.fake.com",
                "type": "doc",
                "title": "Sample Material 2"
            }
        }
        quiz = {
            "title": "Fun Quiz",
            "duration": 3600,
            "questions": {
                "1": {
                    "answer": "A",
                    "options": {
                        "A": "Yes",
                        "B": "No"
                    },
                    "question": "Is engineering fun?"
                },
                "2": {
                    "answer": "D",
                    "options": {
                        "A": "He is hungry",
                        "B": "He has too much work to do",
                        "C": "He doesn't know what to do with his life",
                        "D": "All of the above"
                    },
                    "question": "Why is Rafe sad?"
                }
            }
        }
        self.chapter = Chapter.objects.create(
            chapter_no=1, title="Title", description="Description", course_id=1, course_class_id=1, quiz=quiz,
            materials=materials)

    def tearDown(self):
        self.chapter = None

    def test_get_chapter_in_class(self):
        response = client.get(
            reverse(
                "get_chapter_in_class",
                kwargs={"classroom_id": self.chapter.course_class_id,
                        "chapter_no": self.chapter.chapter_no}))
        chapter = Chapter.objects.get(
            course_class=self.chapter.course_class_id, chapter_no=self.chapter.chapter_no)
        serializer = ChapterSerializer(chapter)
        self.assertEqual(json.loads(json.dumps(response.data))[0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_chapter_in_class(self):
        response = client.get(
            reverse(
                "get_chapter_in_class",
                kwargs={"classroom_id": self.chapter.course_class_id, "chapter_no": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_class_of_chapter(self):
        response = client.get(
            reverse(
                "get_chapter_in_class",
                kwargs={"classroom_id": 999, "chapter_no": self.chapter.chapter_no}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewChapterTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            username="testUser", display_name="testUser", is_admin=True)
        self.course = Course.objects.create(
            course_name="test course", description="description", is_active=True)
        self.classroom = Classroom.objects.create(
            class_name="g99", course_id=1, start_datetime=date.today(),
            end_datetime=date.today(),
            trainer_id=self.profile.pk, enroll_start=date.today(),
            enroll_end=date.today(),
            class_size=30)
        self.validPayload = {"chapter_no": 1, "title": "Title", "description": "Description",
                             "course_id": self.classroom.course_id, "course_class_id": self.classroom.pk}
        self.incompletePayload = {
            "chapter_no": 1, "title": "Title", "description": "Description", "course_id": 1}
        self.invalidPayload = {"chapter_no": 1, "title": "Title",
                               "description": "Description", "course_id": 999, "course_class_id": 999}

    def tearDown(self):
        self.course = None
        self.classroom = None
        self.validPayload = None
        self.incompletePayload = None
        self.invalidPayload = None

    def test_create_chapter_successfully(self):
        response = client.post(reverse("create_new_chapter"), data=json.dumps(
            self.validPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_chapter_incomplete_payload(self):
        response = client.post(reverse("create_new_chapter"), data=json.dumps(
            self.incompletePayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_chapter_invalid_payload(self):
        response = client.post(reverse("create_new_chapter"), data=json.dumps(
            self.invalidPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateChapterTest(TestCase):
    def setUp(self):
        materials = {
            "0": {
                "url": "s3.bucket.fake.com",
                "type": "pdf",
                "title": "Sample Material"
            },
            "1": {
                "url": "s3.bucket.fake.com",
                "type": "doc",
                "title": "Sample Material 2"
            }
        }
        quiz = {
            "title": "Fun Quiz",
            "duration": 3600,
            "questions": {
                "1": {
                    "answer": "A",
                    "options": {
                        "A": "Yes",
                        "B": "No"
                    },
                    "question": "Is engineering fun?"
                },
                "2": {
                    "answer": "D",
                    "options": {
                        "A": "He is hungry",
                        "B": "He has too much work to do",
                        "C": "He doesn't know what to do with his life",
                        "D": "All of the above"
                    },
                    "question": "Why is Rafe sad?"
                }
            }
        }
        self.chapter = Chapter.objects.create(
            chapter_no=1, title="Title", description="Description", course_id=1, course_class_id=1, quiz=quiz,
            materials=materials)

        self.validPayload = {
            "chapter_id": self.chapter.id,
            "title": "Changed title",
            "description": "Changed description"
        }

        self.invalidPayload = {
            "chapter_id": 999,
            "title": "invalid payload",
            "description": "invalid payload"
        }

    def tearDown(self):
        self.chapter = None
        self.validPayload = None
        self.invalidPayload = None

    def test_valid_update_chapter_details(self):
        response = client.patch(reverse("update_chapter"), data=json.dumps(
            self.validPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.validPayload["title"])
        self.assertEqual(response.data["description"],
                         self.validPayload["description"])

    def test_invalid_update_chapter_details(self):
        response = client.patch(reverse("update_chapter"), data=json.dumps(
            self.invalidPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUserProgressTest(TestCase):
    def setUp(self):
        completed_material = {"firebase.starge.url1": True, "firebase.starge.url2": False,
                              "firebase.starge.url3": True, "firebase.starge.url4": False}
        quiz_response = {
            "score": 3,
            "questions":
            {"1": {"correct": "true", "response": "B", "correct_answer": "B"},
             "2": {"correct": "false", "response": "B", "correct_answer": "A"},
             "3": {"correct": "false", "response": "B", "correct_answer": "A"},
             "4": {"correct": "true", "response": "A", "correct_answer": "A"},
             "5": {"correct": "true", "response": "C", "correct_answer": "C"}},
            "total_score": 5}
        self.progress = Progress.objects.create(learner_id="rafeang", chapter_id=8,
                                                completed_material=completed_material, quiz_response=quiz_response)

    def tearDown(self):
        self.progress = None

    def test_get_user_progress(self):
        response = client.get(
            reverse(
                "get_user_progress",
                kwargs={"chapter_id": self.progress.chapter_id,
                        "username": self.progress.learner_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateUserProgressTest(TestCase):
    def setUp(self):
        completed_material = {"firebase.starge.url1": True, "firebase.starge.url2": False,
                              "firebase.starge.url3": True, "firebase.starge.url4": False}
        quiz_response = {
            "score": 3,
            "questions":
            {"1": {"correct": "true", "response": "B", "correct_answer": "B"},
             "2": {"correct": "false", "response": "B", "correct_answer": "A"},
             "3": {"correct": "false", "response": "B", "correct_answer": "A"},
             "4": {"correct": "true", "response": "A", "correct_answer": "A"},
             "5": {"correct": "true", "response": "C", "correct_answer": "C"}},
            "total_score": 5}
        self.progress = Progress.objects.create(learner_id="rafeang", chapter_id=9,
                                                completed_material=completed_material, quiz_response=quiz_response)
        self.validPayload = {
            "learner": self.progress.learner_id,
            "chapter": self.progress.chapter_id,
            "completed_material": {
                "firebase_storage_url1": False,
                "firebase_storage_url2": False,
            }
        }

        # no such learner
        self.invalidPayload = {
            "learner": "learner1",
            "chapter": 1,
            "completed_material": {
                "firebase_storage_url1": True,
                "firebase_storage_url2": False
            }
        }

    def tearDown(self):
        self.progress = None

    def test_update_valid_user_progress(self):
        response = client.put(reverse("update_user_progress"), data=json.dumps(
            self.validPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_user_progress(self):
        response = client.put(reverse("update_user_progress"), data=json.dumps(
            self.invalidPayload), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
