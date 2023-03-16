from django.db.models.aggregates import Count
from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import *
from ..serializers import *
import logging
logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_chapter_by_id(request, chapter_id):
    """
    Retrieve chapter by chapter_id
    """
    try:
        return get_by_pk(Chapter, chapter_id, ChapterSerializer, request)
    except Chapter.DoesNotExist:
        return Response("No Chapter found", status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_chapters_in_class(request, classroom_id):
    """
    Retrieve all chapters in a specified classroom
    """
    try:
        # Check if classroom exists
        classroom_exists = Classroom.objects.filter(id=classroom_id)
    except Classroom.DoesNotExist:
        return Response("No Classroom found", status.HTTP_404_NOT_FOUND)

    try:
        # Filter chapters by classroom id
        filtered_chapters = Chapter.objects.filter(
            course_class_id=classroom_id)

        chapters = ChaptersSerializer(filtered_chapters, context={
                                      'request': request}, many=True)
        return Response(chapters.data, status.HTTP_200_OK)
    except Chapter.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_chapter_in_class(request, classroom_id, chapter_no):
    """
    Retrieve chapter details using classroom_id and chapter_no as identifiers
    """
    try:
        # Check if classroom exists
        Classroom.objects.filter(id=classroom_id)
    except:
        return Response("No classroom found", status=status.HTTP_404_NOT_FOUND)

    # Filter single chapter from class and chapter number
    chapter_info = Chapter.objects.filter(
        course_class_id=classroom_id,
        chapter_no=chapter_no
    )
    chapter = ChapterSerializer(chapter_info, context={
                                'request': request}, many=True)
    if chapter.data != []:
        return Response(chapter.data, status=status.HTTP_200_OK)
    return Response("No chapter found", status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def create_new_chapter(request):
    """
    Creates new chapter
    """
    logger.info('testing info logging')
    try:
        # extract fields from request body
        course_id = request.data["course_id"]
        course_class_id = request.data["course_class_id"]
        chapter_no = request.data["chapter_no"]
        title = request.data["title"]
        description = request.data["description"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # check for valid course and class before creating chapter
    try:
        Course.objects.get(pk=course_id)
        Classroom.objects.get(pk=course_class_id)
    except Course.DoesNotExist or Classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Create chapter information
    try:
        data = {"course": course_id, "course_class": course_class_id,
                "chapter_no": chapter_no, "title": title, "description": description}
        logger.info('line 1 passed')
        serializer = ChapterSerializer(data=data, partial=True)
        logger.info('line 2 passed')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.info('something fk up')
        logger.error(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
def update_chapter(request):
    """
    Update chapter details
    """
    # Check if chapter_id is in request body and retrieve chapter object
    try:
        chapter_id = request.data["chapter_id"]
        chapter = Chapter.objects.get(pk=chapter_id)
    except Chapter.DoesNotExist:
        return Response("Chapter not found", status=status.HTTP_400_BAD_REQUEST)

    # Update chapter instance with new data
    try:
        serializer = ChapterSerializer(
            instance=chapter, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def user_progress(request, chapter_id, username):
    """
    Retrieve user's progress for a chapter in a class
    """
    try:
        chap_prog = Progress.objects.get(chapter=chapter_id, learner=username)
        serializer = ProgressSerializer(
            chap_prog, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Progress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_progress(request):
    """
    Update learner's material progress for a chapter
    """
    username = request.data["learner"]
    chapter_id = request.data["chapter"]

    try:
        current_progress = Progress.objects.get(
            learner=username, chapter=chapter_id)
    except Progress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProgressSerializer(
        current_progress, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
