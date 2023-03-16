from django.db import models
from django.db.models import Max
from .course import Course
from .classroom import Classroom

class ChapterManager(models.Manager):
    def num_chapters(self, course_class_id):
        return super().get_queryset().filter(course_class_id=course_class_id).aggregate(Max('chapter_no'))["chapter_no__max"]

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    chapter_no = models.IntegerField(default=0, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    quiz = models.JSONField(default=dict, null=True, blank=True)
    materials = models.JSONField(default=dict, null=True, blank=True)
    objects = ChapterManager()

    def __str__(self):
        return "Course: " + str(self.course.id) + ", Class: " + self.course_class.class_name + ", Chapter: " + str(self.chapter_no)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['course', 'course_class', 'chapter_no'], name = 'chapter_cpk')
        ]