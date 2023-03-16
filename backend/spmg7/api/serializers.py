from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import *
import json


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description']


class PreReqSerializer(serializers.ModelSerializer):
    course_main = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)
    pre_requisite = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)

    class Meta:
        model = PreReq
        fields = ['id', 'course_main', 'pre_requisite']


class ClassroomSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)

    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'course', 'start_datetime', 'end_datetime',
                  'enroll_start', 'enroll_end', 'class_size', 'trainer']


class ChapterSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)
    course_class = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=False)

    class Meta:
        model = Chapter
        fields = ['id', 'course', 'course_class', 'chapter_no', 'title', 'description', 'materials', 'quiz']


class ChaptersSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)
    course_class = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=False)

    class Meta:
        model = Chapter
        fields = ['id', 'course', 'course_class', 'chapter_no', 'title', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'is_admin']


class GetEnrollmentSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=False)
    course_class = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=False)
    course_id = serializers.SerializerMethodField()

    def get_course_id(self, obj):
        classroom = Classroom.objects.filter(pk=obj.course_class_id)
        serializer = ClassroomSerializer(classroom, many=True)
        query = dict(serializer.data[0].items())
        return query["course"]

    class Meta:
        model = Enrollment
        fields = ['id', 'username', 'course_class', 'course_id', 'current_chapter', 'status']


class EnrollmentSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=False)
    course_class = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=False)

    class Meta:
        model = Enrollment
        fields = ['id', 'username', 'course_class', 'current_chapter', 'status']


class ProgressSerializer(serializers.ModelSerializer):
    learner = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=False)
    chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), many=False)

    class Meta:
        model = Progress
        fields = ['id', 'learner', 'chapter', 'completed_material', 'quiz_response']


class TrainerCourseSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)

    class Meta:
        model = Classroom
        fields = ['id', 'course_id', 'class_size', 'trainer']
