from django.db import models

# Ignore for now, authentication to be done by Azure Directory SSO


class Profile(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    display_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
