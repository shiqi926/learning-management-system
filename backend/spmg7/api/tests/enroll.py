import json
from django.test import TestCase, Client, client
from ..serializers import *
from ..models import *
from django.urls import reverse
from rest_framework import status
import datetime
import json

client = Client()


class GetEligibleLearnersTest(TestCase):
    """ Test GET list of elgiible learners API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.course1 = Course.objects.create(course_name="prog l", description="intermediate programming")
        self.course1.pre_req.add(self.course.pk)

        self.trainer = Profile.objects.create(username="andreee", display_name="Andre Lim")
        self.trainer1 = Profile.objects.create(username="charles", display_name="Charles Lim")

        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.trainer, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.classroom1 = Classroom.objects.create(
            course=self.course1, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.trainer, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)

        self.enroll = Enrollment.objects.create(username=self.trainer, course_class=self.classroom, current_chapter=1)
        self.enroll = Enrollment.objects.create(username=self.trainer1, course_class=self.classroom, current_chapter=1)
        self.enroll = Enrollment.objects.create(username=self.trainer, course_class=self.classroom1, current_chapter=1)
        self.enroll = Enrollment.objects.create(username=self.trainer1, course_class=self.classroom1, current_chapter=1)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_eligible_learners_with_pre_req(self):
        response = client.get(reverse('get_eligible_learners', kwargs={'course_id': self.course1.pk}))
        course1_pre_req = PreReq.objects.filter(course_main_id=self.course1.pk).values("pre_requisite_id")
        course_class = Classroom.objects.filter(course_id=self.course1.pk).values("id")
        pre_req_class = Classroom.objects.filter(course_id__in=course1_pre_req).values("id")
        learners = Profile.objects.filter(enrollment__in=Enrollment.objects.filter(
            course_class_id__in=pre_req_class, status="P")).exclude(
            enrollment__in=Enrollment.objects.filter(course_class_id__in=course_class, status=["P", "IP"]))

        serializer = ProfileSerializer(learners, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eligible_learners_without_pre_req(self):
        response = client.get(reverse('get_eligible_learners', kwargs={'course_id': self.course.pk}))
        course_pre_req = PreReq.objects.filter(course_main=self.course).values("pre_requisite_id")
        pre_req_class = Classroom.objects.filter(course_id__in=course_pre_req).values("id")
        learners = Profile.objects.exclude(enrollment__in=Enrollment.objects.filter(
            course_class_id__in=pre_req_class, status="P"))
        serializer = ProfileSerializer(learners, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostEnrollLearnersTest(TestCase):
    """ Test POST HR enroll learners & learners self enroll API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        self.user1 = Profile.objects.create(username="charles", display_name="Charles Lim")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.payload_hr = {"learners": [
            {
                "username": self.user.pk,
                "course_class": self.classroom.pk,
                "status": "IP"
            },
            {
                "username": self.user1.pk,
                "course_class":  self.classroom.pk,
                "status": "IP"
            }
        ]}
        self.invalid_payload_hr_learner = {"learners": [
            {
                "username": "annie",
                "course_class": self.classroom.pk,
                "status": "IP"
            }
        ]}
        self.invalid_payload_hr_classroom = {"learners": [
            {
                "username": self.user.pk,
                "course_class": 999,
                "status": "IP"
            }
        ]}
        self.invalid_payload_hr_status = {"learners": [
            {
                "username": self.user.pk,
                "course_class": self.classroom.pk,
                "status": "HI"
            }
        ]}
        self.payload_learner = {"learners": [
                                {
                                    "username": self.user1.pk,
                                    "course_class": self.classroom.pk,
                                    "status": "P"
                                }
                                ]}

    def tearDown(self) -> None:
        return super().tearDown()

    def test_create_valid_enroll_hr(self):
        response = client.post(
            reverse('post_enroll_learners'),
            data=json.dumps(self.payload_hr),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_enroll_learner(self):
        response = client.post(
            reverse('post_enroll_learners'),
            data=json.dumps(self.payload_learner),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_enroll_hr_learner(self):
        response = client.post(reverse('post_enroll_learners'), data=json.dumps(
            self.invalid_payload_hr_learner), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_enroll_hr_classroom(self):
        response = client.post(reverse('post_enroll_learners'), data=json.dumps(
            self.invalid_payload_hr_classroom), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_enroll_hr_status(self):
        response = client.post(
            reverse('post_enroll_learners'),
            data=json.dumps(self.invalid_payload_hr_status),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HrActionTest(TestCase):
    """ Test HR approve/reject API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.enroll = Enrollment.objects.create(username=self.user, course_class=self.classroom, status="P")
        self.valid_payload_IP = {"learners": [
            {
                "enrollment_id": self.enroll.pk,
                "status": "IP"
            }
        ]
        }

        self.valid_payload_R = {"learners": [
            {
                "enrollment_id": self.enroll.pk,
                "status": "IP"
            }
        ]
        }

        self.invalid_payload = {"learners": [
            {
                "enrollment_id": 999,
                "status": "R"
            }
        ]
        }

    def tearDown(self) -> None:
        return super().tearDown()

    def test_hr_approve(self):
        response = client.put(
            reverse("put_hr_action_learners"),
            data=json.dumps(self.valid_payload_IP),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hr_reject(self):
        response = client.put(
            reverse("put_hr_action_learners"),
            data=json.dumps(self.valid_payload_R),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hr_invalid(self):
        response = client.put(
            reverse("put_hr_action_learners"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetPendingEnrollmentTest(TestCase):
    """ Test GET pending enrollment API """

    def setUp(self):
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.enroll = Enrollment.objects.create(username=self.user, course_class=self.classroom, status="P")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_pending_enrollment(self):
        response = client.get(reverse("get_pending_enrollment"))
        enroll = Enrollment.objects.filter(status="PD")
        serializer = EnrollmentSerializer(enroll, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetTrainersTest(TestCase):
    """ Test GET Trainers API """

    def setUp(self):
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim", is_admin=True)
        self.user = Profile.objects.create(username="shiqii", display_name="Shikira")
        self.user = Profile.objects.create(username="rafeee", display_name="Rafu")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_all_trainers(self):
        response = client.get(reverse("get_trainers"))
        trainers = Profile.objects.filter(is_admin=False)
        serializer = ProfileSerializer(trainers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AssignTrainerTest(TestCase):
    """ Test POST Trainer API """

    def setUp(self):
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        self.user1 = Profile.objects.create(username="shiqii", display_name="Shikira")
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.valid_payload = {
            "course_class": 2,
            "trainers": [self.user1.username]
        }
        self.invalid_payload = {
            "course_class": 2,
            "trainers": ["ytyt"]
        }

    def tearDown(self) -> None:
        return super().tearDown()

    def test_valid_trainers(self):
        response = client.post(
            reverse("post_assign_trainer"),
            data=json.dumps(self.valid_payload),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_trainers(self):
        response = client.post(
            reverse("post_assign_trainer"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUserEnrolledTest(TestCase):
    """ Test GET user enrolled classes API """

    def setUp(self):
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        self.user1 = Profile.objects.create(username="shiqii", display_name="Shikira")
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.enroll = Enrollment.objects.create(username=self.user1, course_class=self.classroom, status="IP")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_valid_user_enrolled(self):
        response = client.get(reverse("get_user_enrolled", kwargs={"username": self.user1.pk}))
        user_enrolled = Enrollment.objects.filter(username_id=self.user1.pk)
        serializer = GetEnrollmentSerializer(user_enrolled, many=True)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_enrolled(self):
        response = client.get(reverse("get_user_enrolled", kwargs={"username": "IS212"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetClassLearnersTest(TestCase):
    """ Test GET list of learners enrolled in a class API """

    def setUp(self):
        self.user = Profile.objects.create(username="andreee", display_name="Andre Lim")
        self.user1 = Profile.objects.create(username="shiqii", display_name="Shikira")
        self.user2 = Profile.objects.create(username="charlesss", display_name="Chalrsez")
        self.course = Course.objects.create(course_name="intro prog", description="intro to programming")
        myStr = "2021-10-01 15:26"
        current_date_time = datetime.datetime.strptime(myStr, "%Y-%m-%d %H:%M")
        self.classroom = Classroom.objects.create(
            course=self.course, class_name="g1", start_datetime=current_date_time, end_datetime=current_date_time,
            trainer=self.user, enroll_start=current_date_time, enroll_end=current_date_time, class_size=30)
        self.enroll = Enrollment.objects.create(username=self.user1, course_class=self.classroom, status="IP")
        self.enroll = Enrollment.objects.create(username=self.user2, course_class=self.classroom, status="IP")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_valid_class_enrolled(self):
        response = client.get(reverse("get_class_enrolled_learners", kwargs={"course_class_id": self.classroom.pk}))
        enroll = Enrollment.objects.filter(course_class_id=self.classroom.pk, status="IP")
        serializer = GetEnrollmentSerializer(enroll, many=True)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_class_enrolled(self):
        response = client.get(reverse("get_class_enrolled_learners", kwargs={"course_class_id": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
