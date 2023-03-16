# TDD: rafe.ang.2019
import json
from django.test import TestCase, Client
from ..serializers import ChapterSerializer
from ..models import Chapter, Progress, Enrollment
from django.urls import reverse
from rest_framework import status

client = Client()

class CreateQuizTest(TestCase):
  """ Test POST quiz API """ 
  def setUp(self):
    materials = { "0": { "url": "s3.bucket.fake.com", "type": "pdf", "title": "Sample Material" } }
    self.chapter = Chapter.objects.create(chapter_no=1, title="Title", description="Description", course_id=1, course_class_id=3, materials=materials)
    quiz = { "title": "Test", "duration": 3600, "questions": { "1": { "answer": "Yes", "options": ["Yes", "No"], "question": "Good?" } } }
    self.payload = { "chapter_id": self.chapter.pk, "quiz": quiz, "trainer_id": "yingting" }
    self.invalid_trainer_payload = { "chapter_id": self.chapter.pk, "quiz": quiz, "trainer_id": "rafeang" }
    self.invalid_chapter_payload = { "chapter_id": 999, "quiz": quiz, "trainer_id": "charleslim" }

  def tearDown(self):
    self.chapter = None
    self.payload = None
    self.invalid_chapter_payload = None
    self.invalid_trainer_payload = None

  def test_create_quiz(self):
    response = client.post(reverse('create_quiz'), data = json.dumps(self.payload), content_type="application/json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_invalid_trainer(self):
    response = client.post(reverse("create_quiz"), data=json.dumps(self.invalid_trainer_payload), content_type="application/json")
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_invalid_chapter(self):
    response = client.post(reverse("create_quiz"), data=json.dumps(self.invalid_chapter_payload), content_type="application/json")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetQuizTest(TestCase):
  """ Test GET quiz API """
  def setUp(self):
    quiz = { "title": "Test", "duration": 3600, "questions": { "1": { "answer": "Yes", "options": ["Yes", "No"], "question": "Good?" } } }
    materials = { "0": { "url": "s3.bucket.fake.com", "type": "pdf", "title": "Sample Material" } }
    self.chapter = Chapter.objects.create(chapter_no=1, title="Title", description="Description", course_id=1, course_class_id=1, quiz=quiz, materials=materials)

  def tearDown(self):
    self.chapter = None

  def test_get_quiz(self):
    response = client.get(reverse('get_quiz', kwargs={'id': self.chapter.pk }))
    chapter = Chapter.objects.get(pk=self.chapter.pk)
    serializer = ChapterSerializer(chapter)
    self.assertEqual(response.data, serializer.data["quiz"])
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_invalid_chapter(self):
    response = client.get(reverse('get_quiz', kwargs={'id': 999}))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SubmitQuizTest(TestCase):
    """ Test submit quiz API """
    def setUp(self):
      materials = { "0": { "url": "s3.bucket.fake.com", "type": "pdf", "title": "Sample Material" } }
      quiz = { "title": "Test", "duration": 3600, "questions": { "1": { "answer": "Yes", "options": ["Yes", "No"], "question": "Good?" }, "2": { "answer": "No", "options": ["Yes", "No"], "question": "Bad?" } } }
      self.chapter = Chapter.objects.create(chapter_no=1, title="Title", description="Description", course_id=1, course_class_id=1, materials=materials, quiz=quiz)
      completed_material = {"firebase.starge.url1": True, "firebase.starge.url2": False }
      self.progress = Progress.objects.create(completed_material=completed_material, chapter_id=self.chapter.pk, learner_id="rafeang")
      self.enrollment = Enrollment.objects.create(current_chapter=1, status="IP", username_id="rafeang", course_class_id=2)
      responses = { "1": "No", "2": "All of the above" }
      self.payload = { "responses": responses, "user_id": "rafeang", "chapter_id": self.chapter.pk }
      invalid_response = { "1": "No", "3": "All of the above" }
      self.invalid_payload = { "responses": invalid_response, "user_id": "rafeang", "chapter_id": self.chapter.pk }

    def tearDown(self):
      self.progress = None
      self.enrollment = None
      self.chapter = None
      self.payload = None
      self.invalid_payload = None

    def test_submit_quiz(self):
      response = client.post(reverse("submit_quiz"), data=json.dumps(self.payload), content_type="application/json")
      self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_submit_invalid_response(self):
      response = client.post(reverse("submit_quiz"), data=json.dumps(self.invalid_payload), content_type="application/json")
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetQuizResultsTest(TestCase):
  """ Test GET quiz results API """
  def setUp(self):
    quiz_response = { "score": 3, "total_score": 5, "questions": { "1": { "correct_answer": "A", "response":"A", "correct": True } } }
    self.progress = Progress.objects.create(chapter_id=7, learner_id="rafeang", quiz_response=quiz_response)

  def tearDown(self):
    self.progress = None

  def test_get_quiz_results(self):
    response = client.get(reverse('get_quiz_results', kwargs={ 'learner_id': "rafeang", "chapter_id": 7 }))
    progress = Progress.objects.get(learner_id="rafeang", chapter_id=7)
    self.assertEqual(response.data, progress.quiz_response)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_invalid_learner(self):
    response = client.get(reverse('get_quiz_results', kwargs={ 'learner_id': "dooby", "chapter_id": 2 }))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
