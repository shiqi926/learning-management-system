from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Course, PreReq, Profile, Classroom
from ..serializers import CourseSerializer
from ..views.helpers.basic_crud import *
import datetime

# initialize the APIClient app
client = Client()


class GetAllCoursesTest(TestCase):
    """ Test GET quiz API """

    def setup(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.course = Course.objects.create(course_name="prog l", description="intermediate programming")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_courses(self):
        response = client.get(reverse('get_all_courses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetPreRequisiteTest(TestCase):
    """ Test GET pre-requisite API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.course1 = Course.objects.create(course_name="prog l", description="intermediate programming")
        self.course1.pre_req.add(self.course.pk)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_pre_req(self):
        response = client.get(reverse('get_pre_req', kwargs={'course_id': self.course1.pk}))
        course1_pre_req = PreReq.objects.filter(course_main=self.course1).values("pre_requisite_id")
        pre_req = Course.objects.filter(id__in=course1_pre_req)
        serializer = CourseSerializer(pre_req, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_pre_req(self):
        response = client.get(reverse('get_pre_req', kwargs={'course_id': self.course.pk}))
        self.assertEqual([], response.data)


class GetCourseClassDetailsTest(TestCase):
    """ Test GET course class details API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.trainer = Profile.objects.create(username="andreee", display_name="Charles Lim")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.trainer, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)

        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g2", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.trainer, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_pre_req(self):
        response = client.get("/api/courses/class/?course_id=" + str(self.course.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
