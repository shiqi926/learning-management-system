from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from ..models import *
from ..serializers import *
import json


@api_view(['GET'])
def eligible_learners(request, course_id):
    """
    List all users who fulfill the pre-reqs and have not taken the course
    """
    try:
        pre_req = PreReq.objects.filter(course_main_id=course_id).values("pre_requisite_id")
        course_class = Classroom.objects.filter(course_id=course_id).values("id")

        # no pre reqs
        if not pre_req:
            learners = Profile.objects.filter(
                ~ (Q(enrollment__course_class_id__in=course_class) &
                    (Q(enrollment__status="P") & Q(enrollment__status="IP"))
                   ))
            serializer = ProfileSerializer(
                learners, context={'request': request}, many=True)
            return Response(serializer.data)

        try:
            pre_req_class = Classroom.objects.filter(
                course_id__in=pre_req).values("id")

            learners = Profile.objects.filter(enrollment__in=Enrollment.objects.filter(course_class_id__in=pre_req_class, status="P")).exclude(enrollment__in=Enrollment.objects.filter(course_class_id__in=course_class, status=["P","IP"]))

            serializer = ProfileSerializer(learners, context={'request': request}, many=True)
            return Response(serializer.data)
        except Classroom.DoesNotExist or Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    except PreReq.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def check_eligibility(request, course_id, learner_id):
    try:
        pre_req = PreReq.objects.filter(course_main_id=course_id).values("pre_requisite_id")
        course_class = Classroom.objects.filter(course_id=course_id).values("id")

        # no pre reqs
        if not pre_req:
            learners = Profile.objects.filter(
                ~ (Q(enrollment__course_class_id__in=course_class) & 
                    (Q(enrollment__status="P") & Q(enrollment__status="IP"))
                ))
        # has pre reqs
        else:
            try:
                pre_req_class = Classroom.objects.filter(course_id__in=pre_req).values("id")
                learners = Profile.objects.filter(enrollment__in=Enrollment.objects.filter(course_class_id__in=pre_req_class, status="P")).exclude(enrollment__in=Enrollment.objects.filter(course_class_id__in=course_class, status=["P","IP"]))

            except Classroom.DoesNotExist or Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND) 
        for user in learners.iterator():
            if user.username == learner_id:
                return Response(data=True, status=status.HTTP_200_OK)
        return Response(data=False, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])    
def enroll_learners(request):
    """
    HR enroll learners in batch, or
    Learners self enroll
    """
    learners = request.data["learners"]

    for learner in learners:
        serializer = EnrollmentSerializer(data=learner)
        if serializer.is_valid():
            # check if user has already registered for another class in the course
            # get course of class
            course_id = Classroom.objects.filter(
                pk=learner["course_class"])[0].course_id
            course_class_list = [
                course_class.id for course_class in Classroom.objects.filter(course_id=course_id)]
            learner_enrollment = Enrollment.objects.filter(
                username_id=learner["username"],
                course_class_id__in=course_class_list
            )
            if len(learner_enrollment) > 0:
                return Response("Learner already enrolled in the course", status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            if learner["status"] == "IP":
                chapters = Chapter.objects.filter(
                    course_class_id=learner["course_class"])
                for chapter in chapters:
                    material = {}
                    chap_id = chapter.id
                    materials = chapter.materials

                    for key, m in materials.items():
                        material[m["url"]] = False

                    user = Profile.objects.get(username=learner["username"]).pk
                    this_chapter = Chapter.objects.get(id=chap_id).pk
                    data_prog = {
                        "learner": user,
                        "chapter": this_chapter,
                        "completed_material": material
                    }
                    dj = json.dumps(data_prog)
                    data_json = json.loads(dj)
                    serializer_progress = ProgressSerializer(data=data_json)
                    if serializer_progress.is_valid():
                        serializer_progress.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def hr_action_learners(request):
    """
    HR approve/ reject selected learners
    """
    learners = request.data["learners"]

    for learner in learners:
        try:
            enrollment = Enrollment.objects.get(pk=learner["enrollment_id"])
        except Enrollment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        learner["username"] = enrollment.username.username
        learner['course_class'] = enrollment.course_class.id
        serializer = EnrollmentSerializer(
            enrollment, data=learner, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            if learner["status"] == "IP":
                chapters = Chapter.objects.filter(
                    course_class_id=learner["course_class"])
                for chap in chapters:
                    mat = {}
                    chap_id = chap.id
                    materials = chap.materials

                    for key, m in materials.items():
                        mat[m["url"]] = False

                    user = Profile.objects.get(pk=learner["username"]).pk
                    this_chapter = Chapter.objects.get(pk=chap_id).pk
                    data_prog = {
                        "learner": user,
                        "chapter": this_chapter,
                        "completed_material": mat
                    }
                    dj = json.dumps(data_prog)
                    data_json = json.loads(dj)
                    serializer_progress = ProgressSerializer(data=data_json)
                    if serializer_progress.is_valid():
                        serializer_progress.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)


@api_view(['GET'])
def pending_enrollment(request):
    """
    Retrieve enrollments with status = Pending ("PD")
    """
    try:
        enrollment = Enrollment.objects.filter(status="PD")
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EnrollmentSerializer(
        enrollment, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_trainers(request):
    """
    List users where isAdmin=False
    """
    try:
        profile = Profile.objects.filter(is_admin=False)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(
        profile, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def assign_trainer(request):
    """
    HR assign trainers
    """
    trainers = request.data["trainers"]

    for trainer in trainers:
        try:
            course_classroom = Classroom.objects.get(
                pk=request.data["course_class"])
        except Classroom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        req = {
            "class_name": course_classroom.class_name,
            "start_datetime": course_classroom.start_datetime,
            "end_datetime": course_classroom.end_datetime,
            "enroll_start": course_classroom.enroll_start,
            "enroll_end": course_classroom.enroll_end,
            "class_size": course_classroom.class_size,
            "course": course_classroom.course_id,
            "trainer": trainer
        }
        serializer = ClassroomSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


@api_view(['GET'])
def user_enrolled_classes(request, username):
    """
    Retrieve enrollments for user where status=In progress ("IP")
    """
    try:
        profile = Profile.objects.get(pk=username)
        enrollment = Enrollment.objects.filter(
            username_id=username, status="IP")
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GetEnrollmentSerializer(
        enrollment, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def class_enrolled_learners(request, course_class_id):
    """
    Get list of enrolled learners for a class
    """
    try:
        classroom = Classroom.objects.get(id=course_class_id)
        enroll = Enrollment.objects.filter(
            course_class=course_class_id, status="IP")
    except Classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GetEnrollmentSerializer(
        enroll, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_chapter(request, enrollment_id):
    try:
        current_chapter = Enrollment.objects.filter(
            id=enrollment_id).values('current_chapter')
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(current_chapter, status=status.HTTP_200_OK)
