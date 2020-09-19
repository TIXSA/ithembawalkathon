from datetime import datetime, timedelta

from django.core.mail import send_mail

from ithemba_walkathon import env
from ..clients.firebase import send_message


def handle_model_update(page):
    message = {
        'data': {
            'refresh_app_page': str(page),
        },
        'topic': env.GLOBAL_TOPIC
    }

    send_message(message, True)


def iso_string_to_datetime(iso_date_string):
    return datetime.strptime(iso_date_string, "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=2)


def send_contact_us_message(user_profile, contact_us_form):
    message = ''
    message += '\nApp user id: {} \n'.format(user_profile.id)
    message += '\n========= Form input ======= \n\n'
    message += 'Name: {}  \n'.format(contact_us_form['name'])
    message += 'Email: {}  \n'.format(contact_us_form['contact'])
    message += 'Message: {}  \n\n'.format(contact_us_form['message'])
    send_mail(
        'New app Contact Us Form message',
        message,
        env.EMAIL_HOST_USER,
        [env.CONTACT_US_EMAIL, '0760621827@winsms.net'],
        fail_silently=False,
    )
