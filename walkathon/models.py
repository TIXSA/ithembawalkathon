from django.db import models
from django.conf import settings


class Walker(models.Model):
    walker_number = models.CharField(max_length=255, null=True)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    distance_to_walk = models.CharField(max_length=255, null=True)
    fcm_token = models.TextField()
    total_walked_distance = models.CharField(max_length=255, null=True)
    walk_method = models.CharField(max_length=255, null=True)
    team = models.CharField(max_length=255, null=True)
    pace = models.CharField(max_length=255, null=True)
    device_type = models.CharField(max_length=20, null=True)
    new_notification = models.BooleanField(default=False)
    time_started = models.TimeField(null=True)
    time_ended = models.TimeField(null=True)
    total_received_notifications = models.IntegerField(default=0)
    total_opened_notifications = models.IntegerField(default=0)

    def __str__(self):
        return self.walker_number


class Walkathon(models.Model):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    starting_time = models.TimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)


class SystemMessages(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    time_to_be_sent = models.TimeField(null=True)
    message_type = models.CharField(max_length=255)  # blast or targeted
    message_sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)


class UserMessages(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_sent = models.TimeField(null=True)
    message_type = models.CharField(max_length=255)
