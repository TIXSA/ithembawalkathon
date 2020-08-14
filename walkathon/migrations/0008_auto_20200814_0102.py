# Generated by Django 2.1.4 on 2020-08-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walkathon', '0007_auto_20200814_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemmessages',
            name='message_type',
            field=models.CharField(choices=[('Individual', 'System Generated Walker Activity Related'), ('Blast', 'Marketing Team')], max_length=255),
        ),
        migrations.AlterField(
            model_name='systemmessages',
            name='time_to_be_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='message_type',
            field=models.CharField(default='Individual', max_length=255),
        ),
    ]
