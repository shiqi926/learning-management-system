from rest_framework.serializers import Serializer
from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Course, PreReq
from ..serializers import *
from drf_multiple_model.views import ObjectMultipleModelAPIView


@api_view(['GET'])
def get_course_by_id(request, course_id):
    """
    Retrieve course by id
    """
    try:
        classroom = Course.objects.filter(pk=course_id)
        serializer = CourseSerializer(classroom, context={'request': request}, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def all_courses(request):
    """
    List all active courses
    """
    return get_all_paginated(Course, 10, '/api/courses/?page=', CourseSerializer, request)


@api_view(['GET'])
def pre_req(request, course_id):
    """
    Get pre-requisite of a course
    """

    try:
        pre_req_id = PreReq.objects.filter(course_main=course_id).values("pre_requisite_id")
        pre_req = Course.objects.filter(id__in=pre_req_id)
        serializer = CourseSerializer(pre_req, context={'request': request}, many=True)
        return Response(serializer.data)

    except Course.DoesNotExist or PreReq.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CourseClassAPIView(ObjectMultipleModelAPIView):
    def get_querylist(self):
        course_id = self.request.query_params['course_id']
        course_obj = Course.objects.filter(id=course_id)

        course_obj_id = Course.objects.get(id=course_id).id

        query_list = [
            {'queryset': course_obj, 'serializer_class': CourseSerializer},
            {'queryset': Classroom.objects.filter(course=course_obj_id), 'serializer_class': ClassroomSerializer}
        ]

        return query_list
