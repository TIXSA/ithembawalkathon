from django.db import models
from django.conf import settings

from walkathon.helpers.system_messages import handle_system_message_update
from walkathon.helpers.common import handle_model_update

MESSAGE_TYPE_CHOICES = (
    ('Individual', 'System Generated and Walker Activity Related'),
    ('Blast', 'Marketing Team'),
)

SEND_CONDITION_CHOICES = (
    ('4km1', '4 km 1st Milestone'),
    ('4km2', '4 km 2nd Milestone'),
    ('4km3', '4 km 3rd Milestone'),
    ('4km4', '4 km 4th Milestone'),
    ('8km1', '8 km 1st Milestone'),
    ('8km2', '8 km 2nd Milestone'),
    ('8km3', '8 km 3rd Milestone'),
    ('8km4', '8 km 4th Milestone'),
    ('NOW', 'SEND NOW - WARNING will send immediately after you press save'),
    ('SCHEDULED', 'Scheduled - Date and Time need to be specified'),
    ('NEW_STREAM_STARTED', 'Stream started'),
)


class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    long_uid = models.IntegerField()
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)
    chooser = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Entrant(models.Model):
    eid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    registration_date = models.DateField(blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    id_no = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    preferred_communication = models.CharField(max_length=50, blank=True, null=True)
    t_shirt_size = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=32, decimal_places=0)
    cancer_survivor = models.CharField(max_length=50, blank=True, null=True)
    representative_or_consultant = models.CharField(max_length=50, blank=True, null=True)
    avon_justine_acc_no = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    earnings_opportunity = models.CharField(max_length=50, blank=True, null=True)
    receive_communication = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    walk_distance = models.CharField(max_length=50, blank=True, null=True)
    register_a_team = models.CharField(max_length=50, blank=True, null=True)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    terms_conditions = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=50, blank=True, null=True)
    area_code = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    str_no = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    street_address_2 = models.CharField(max_length=50, blank=True, null=True)
    street_address_1 = models.CharField(max_length=50, blank=True, null=True)
    delivery_instructions = models.CharField(max_length=1000, blank=True, null=True)
    terms_and_conditions_download = models.CharField(max_length=50, blank=True, null=True)
    passport_no = models.CharField(max_length=50, blank=True, null=True)
    register_by_passport_or_id = models.CharField(max_length=50, blank=True, null=True)
    manual_paid = models.CharField(max_length=50, blank=True, null=True)
    manual_paid_amount = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    payfast_paid = models.CharField(max_length=50, blank=True, null=True)
    last_edited_by = models.IntegerField(blank=True, null=True)
    last_updated_datetime = models.DateTimeField(blank=True, null=True)
    payment_comments = models.TextField(blank=True, null=True)
    payfast_paid_amount = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    despatch_date = models.DateTimeField(blank=True, null=True)
    despatched = models.CharField(max_length=50, blank=True, null=True)
    receipted = models.CharField(max_length=50, blank=True, null=True)
    despatch_comments = models.TextField(blank=True, null=True)
    despatch_last_edit_by = models.IntegerField(blank=True, null=True)
    despatch_last_update_datetime = models.DateTimeField(blank=True, null=True)
    acc_date = models.DateTimeField(blank=True, null=True)
    complete = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrant'


class Teams(models.Model):
    wid = models.AutoField(primary_key=True)
    uid = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    id_no = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    team_name = models.CharField(max_length=50)
    t_shirt_size = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    passport_no = models.CharField(max_length=50, blank=True, null=True)
    register_by_passport_or_id = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    complete = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'


class Walker(models.Model):
    uid = models.IntegerField(default=0)
    walker_number = models.CharField(max_length=255, default=0000)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    distance_to_walk = models.CharField(max_length=255, null=True, default=8)
    fcm_token = models.TextField(null=True, blank=True)
    total_walked_distance = models.IntegerField(null=True, default=0)
    walk_method = models.CharField(max_length=255, null=True, default='Route')
    team = models.CharField(max_length=255, null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True, blank=True)
    steps_walked = models.CharField(max_length=255, null=True, default=0)
    time_started = models.DateTimeField(null=True, blank=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    milestones = models.TextField(null=True, default=[])
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    messages_read = models.TextField(null=True, default=[])
    messages_received = models.TextField(null=True, default=[])
    walker_leader = models.BooleanField(default=False)
    generated_username = models.CharField(max_length=255, null=True, blank=True)
    generated_password = models.CharField(max_length=255, null=True, blank=True)

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

    def save(self, *args, **kwargs):
        handle_model_update('walkathon')
        super(Walkathon, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SystemMessages(models.Model):
    send_condition = models.CharField(max_length=255, default=('4km1', '4 km 1st Milestone'),
                                      choices=SEND_CONDITION_CHOICES)
    time_to_be_sent = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    image_url = models.CharField(null=True, blank=True, max_length=500)
    message_sent = models.BooleanField(default=False)
    message_opened = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        handle_system_message_update(self)
        super(SystemMessages, self).save(*args, **kwargs)


class Streaming(models.Model):
    stream_key = models.CharField(max_length=500)
    year = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    mux_token_id = models.CharField(max_length=255)
    mux_token_secret = models.CharField(max_length=255)
    playback_id = models.CharField(max_length=500)
    stream_id = models.CharField(max_length=500, default='')
    stream_started = models.BooleanField(default=False)
    stream_ended = models.BooleanField(default=False)
    stream_name = models.CharField(max_length=500, default='')

    def save(self, *args, **kwargs):
        handle_model_update('streams')
        super(Streaming, self).save(*args, **kwargs)
