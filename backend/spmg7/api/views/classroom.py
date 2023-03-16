from re import L
from django.db.models.aggregates import Count
from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import *
from ..serializers import *


@api_view(['GET'])
def get_class_by_id(request, classroom_id):
    """
    Retrieve class by id
    """
    try:
        classroom = Classroom.objects.filter(pk=classroom_id)
        serializer = ClassroomSerializer(classroom, context={'request': request}, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_course(request, username):
    """
    Retrieve course taught by trainer
    """
    try:
        courses = Classroom.objects.filter(trainer_id=username)
        serializer = TrainerCourseSerializer(
            courses, context={'request': request}, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_class_in_course(request, username, course_id):
    """
    Retrieve class details of course taught by trainer
    """
    try:
        courses = Classroom.objects.filter(
            trainer_id=username, course_id=course_id)

        serializer = ClassroomSerializer(
            courses, context={'request': request}, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
