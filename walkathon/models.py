from django.db import models
from django.conf import settings

MESSAGE_TYPE_CHOICES = (
        ('Individual', 'System Generated and Walker Activity Related'),
        ('Blast', 'Marketing Team'),
    )

SEND_CONDITION_CHOICES = (
        ('4km1', '4 km 1st Milestone'),
        ('4km2', '4 km 2st Milestone'),
    )


class Walker(models.Model):
    walker_number = models.CharField(max_length=255, default=0000)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    distance_to_walk = models.CharField(max_length=255, null=True,default=8)
    fcm_token = models.TextField(null=True, blank=True)
    total_walked_distance = models.IntegerField(null=True, default=0)
    walk_method = models.CharField(max_length=255, null=True, default='Route')
    team = models.CharField(max_length=255, null=True, blank=True)
    pace = models.CharField(max_length=255, null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True)
    new_notification = models.BooleanField(default=False, blank=True)
    steps_walked = models.CharField(max_length=255, null=True, default=0)
    time_started = models.DateTimeField(null=True, blank=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    total_received_notifications = models.IntegerField(null=True, default=0)
    total_opened_notifications = models.IntegerField(null=True, default=0)
    milestones = models.TextField(null=True, default=[])
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.walker_number


class Walkathon(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    starting_time = models.TimeField()
    starting_day = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class SystemMessages(models.Model):
    message_type = models.CharField(max_length=255, choices=MESSAGE_TYPE_CHOICES)  # blast or targeted
    send_condition = models.CharField(max_length=255, choices=SEND_CONDITION_CHOICES)  # blast or targeted
    time_to_be_sent = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    image_url = models.TextField(null=True, blank=True)
    message_sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)


class UserMessages(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    image_url = models.CharField(max_length=255, null=True, blank=True)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=255, default='Individual')
    message_opened = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)


class Streaming(models.Model):
    stream_key = models.CharField(max_length=500)
    year = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    mux_token_id = models.CharField(max_length=255)
    mux_token_secret = models.CharField(max_length=255)
    playback_id = models.CharField(max_length=500)
    stream_id = models.CharField(max_length=500, default='')
    stream_started = models.BooleanField(default=False)
