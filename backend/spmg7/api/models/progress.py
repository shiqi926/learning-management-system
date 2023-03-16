from django.db import models
from django.db.models.deletion import CASCADE
from .profile import Profile
from .chapter import Chapter

class Progress(models.Model):
    learner = models.ForeignKey(Profile, on_delete=CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=CASCADE)
    completed_material = models.JSONField(default=list)
    quiz_response = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return "Username: " + self.learner.username + ", Chapter: " + self.chapter.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['chapter', 'learner'], name = 'progress_cpk')
        ]