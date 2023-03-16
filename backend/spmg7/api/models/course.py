from django.db import models

class Course(models.Model):
    course_name = models.TextField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    pre_req = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="PreReq"
    )

    def __str__(self):
        return self.course_name

class PreReq(models.Model):
    course_main = models.ForeignKey(Course, related_name="course_main", on_delete=models.CASCADE)
    pre_requisite = models.ForeignKey(Course, related_name="pre_requisite", on_delete=models.CASCADE)