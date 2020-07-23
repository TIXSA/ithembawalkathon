from django.db import models
from django.conf import settings

class Runner(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True, max_length=100)
    password = models.CharField(max_length=100)
    runner_profile = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
