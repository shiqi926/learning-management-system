from django.db import models
from django.db.models.deletion import CASCADE
from .classroom import Classroom
from .profile import Profile

class Enrollment(models.Model):
    PENDING = 'PD'
    REJECTED = "R"
    IN_PROGRESS = 'IP'
    PASSED = 'P'
    FAILED = 'F'
    WITHDRAWN = "W"

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (IN_PROGRESS, 'In Progress'),
        (PASSED, 'Passed'),
        (FAILED, 'Failed'),
        (WITHDRAWN, 'Withdrawn')
    ]

    username = models.ForeignKey(Profile, on_delete=CASCADE)
    course_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    current_chapter = models.PositiveSmallIntegerField(default=1, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        blank=True
    )

    def __str__(self):
        return "Learner: " + self.username.username + ", Course: " + self.course_class.course.course_name + ", Class: " + self.course_class.class_name 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['course_class', 'username'], name = 'enrollment_cpk')
        ]