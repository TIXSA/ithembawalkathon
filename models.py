# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Avonj0011Uggroups(models.Model):
    groupid = models.AutoField(db_column='GroupID', primary_key=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj0011_uggroups'


class Avonj0011Ugmembers(models.Model):
    username = models.CharField(db_column='UserName', primary_key=True, max_length=300)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj0011_ugmembers'
        unique_together = (('username', 'groupid'),)


class Avonj0011Ugrights(models.Model):
    tablename = models.CharField(db_column='TableName', primary_key=True, max_length=300)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    accessmask = models.CharField(db_column='AccessMask', max_length=10, blank=True, null=True)  # Field name made lowercase.
    page = models.TextField(db_column='Page', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj0011_ugrights'
        unique_together = (('tablename', 'groupid'),)


class Avonj001Audit(models.Model):
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=40)
    user = models.CharField(max_length=300, blank=True, null=True)
    table = models.CharField(max_length=300, blank=True, null=True)
    action = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avonj001_audit'


class Avonj001Uggroups(models.Model):
    groupid = models.AutoField(db_column='GroupID', primary_key=True)  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj001_uggroups'


class Avonj001Ugmembers(models.Model):
    username = models.CharField(db_column='UserName', primary_key=True, max_length=300)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj001_ugmembers'
        unique_together = (('username', 'groupid'),)


class Avonj001Ugrights(models.Model):
    tablename = models.CharField(db_column='TableName', primary_key=True, max_length=300)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    accessmask = models.CharField(db_column='AccessMask', max_length=10, blank=True, null=True)  # Field name made lowercase.
    page = models.TextField(db_column='Page', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'avonj001_ugrights'
        unique_together = (('tablename', 'groupid'),)


class Entrant(models.Model):
    eid = models.AutoField(primary_key=True)
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
    avon_justine_acc_no = models.CharField(max_length=50, blank=True, null=True)
    earnings_opportunity = models.CharField(max_length=50, blank=True, null=True)
    receive_communication = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    walk_distance = models.CharField(max_length=50, blank=True, null=True)
    register_a_team = models.CharField(max_length=50, blank=True, null=True)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    terms_conditions = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=50, blank=True, null=True)
    suburb = models.CharField(max_length=50, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    area_code = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)

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

    class Meta:
        managed = False
        db_table = 'teams'


class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Walker(models.Model):
    wid = models.AutoField(primary_key=True)
    eid = models.IntegerField(blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'walker'
