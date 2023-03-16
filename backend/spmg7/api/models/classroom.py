from django.db import models
from .profile import Profile
from .course import Course

class Classroom(models.Model):
    class_name=models.CharField(max_length=3)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField() # must be datetime.date instance
    end_datetime = models.DateTimeField() # must be datetime.date instance
    trainer = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    enroll_start = models.DateTimeField() # must be datetime.date instance
    enroll_end = models.DateTimeField() # must be datetime.date instance
    class_size = models.IntegerField()

    def __str__(self):
        return "Course: " + str(self.course.id) + ", Class: " + self.class_name
