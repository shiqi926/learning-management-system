from rest_framework.serializers import Serializer
from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import *
from ..serializers import *

@api_view(['POST'])
def create_quiz(request):
  """
  Add or update a chapter's quiz
  """
  chapter_id = request.data["chapter_id"]
  trainer_id = request.data["trainer_id"]
  try:
    chapter = Chapter.objects.get(pk=chapter_id)
    course_class_id = chapter.course_class_id
    classroom = Classroom.objects.get(pk=course_class_id)
    if classroom.trainer_id != trainer_id:
      return Response(data=f"{trainer_id} is not an authorised trainer for this class", status=status.HTTP_401_UNAUTHORIZED)
  except Chapter.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  data_to_change = {"quiz": request.data["quiz"]}
  serializer = ChapterSerializer(instance=chapter, data=data_to_change, partial=True)
  if serializer.is_valid(raise_exception=True):
    serializer.save()
  return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_quiz(request, id):
  """
  Get quiz by chapter_id
  """
  try:
    chapter = Chapter.objects.get(pk=id)
  except Chapter.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  return Response(chapter.quiz)

@api_view(["POST"])
def submit_quiz(request):
  """
  Submit quiz response, update enrollment (current_chapter/status) and return results.
  Does an additional 85% pass check if it's for final quiz
  """
  responses = request.data["responses"]
  user_id = request.data["user_id"]
  chapter_id = request.data["chapter_id"]
  try:
    chapter = Chapter.objects.get(pk=chapter_id)
    chapter_num = chapter.chapter_no
    progress = Progress.objects.get(chapter_id=chapter_id, learner_id=user_id)
    course_class_id = chapter.course_class_id
    enrollment = Enrollment.objects.get(course_class_id=course_class_id, username_id=user_id)
  except (Chapter.DoesNotExist, Progress.DoesNotExist, Enrollment.DoesNotExist) as e:
    return Response(status=status.HTTP_404_NOT_FOUND, data=str(e))
  quiz = chapter.quiz["questions"]
  score = 0
  try:
    for num, info in quiz.items():
      ans = info["answer"]
      response = responses[num]
      responses[num] = {}
      responses[num]["response"] = response
      if response == ans:
        responses[num]["correct"] = True
        score += 1
      else:
        responses[num]["correct"] = False
      responses[num]["correct_answer"] = ans
  except KeyError:
    return Response(status=status.HTTP_400_BAD_REQUEST)
  responses["score"] = score
  responses["total_score"] = len(quiz)
  num_chapters = Chapter.objects.num_chapters(course_class_id=course_class_id)
  if chapter_num == -1:
    grade = score / len(quiz)
    if grade >= 0.85:
      responses["result"] = "P"
      enrollment_update = { "status": "P" }
    else:
      responses["result"] = "P"
      enrollment_update = { "status": "IP" }
  else:
    enrollment_update = {"current_chapter": min(chapter_num + 1, num_chapters)}
  e_serializer = EnrollmentSerializer(instance=enrollment, data=enrollment_update, partial=True)
  if e_serializer.is_valid(raise_exception=True):
    e_serializer.save()
  p_serializer = ProgressSerializer(instance=progress, data={ "quiz_response": responses }, partial=True)
  if p_serializer.is_valid(raise_exception=True):
    p_serializer.save()
  return Response(responses)
  
@api_view(['GET'])
def get_quiz_results(request, learner_id, chapter_id):
  """
  Get results by chapter_id and learner_id
  """
  try:
    progress = Progress.objects.get(chapter_id=chapter_id, learner_id=learner_id)
  except Progress.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  return Response(progress.quiz_response)