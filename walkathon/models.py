from django.db import models


class Runner(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True, max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
