from datetime import datetime, timedelta

import bcrypt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from graphql import GraphQLError

import walkathon.helpers.walker as walker_helper
import walkathon.models as models
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
    title = 'New app Contact Us Form message'
    message = '{}'.format(title)
    message += '\n\nApp user id: {} \n'.format(user_profile.id)
    message += '\n========= Form input ======= \n\n'
    message += 'Name: {}  \n'.format(contact_us_form['name'])
    message += 'Email: {}  \n'.format(contact_us_form['contact'])
    message += 'Message: {}  \n\n'.format(contact_us_form['message'])
    send_mail(
        title,
        message,
        env.EMAIL_HOST_USER,
        [env.CONTACT_US_EMAIL],
        fail_silently=False,
    )


def send_password_reset_message(username):
    if not username or not User.objects.filter(username=username).exists():
        raise GraphQLError(env.ERRORS['7'])

    member_django_user = User.objects.filter(username=username).first()
    walker = models.Walker.objects.filter(user_profile=member_django_user).first()
    if not walker.walker_leader:
        raise GraphQLError(env.ERRORS['10'])

    # 1. Generate new password
    generated_password = walker_helper.get_random_alphanumeric_string(10)
    # 2. Update django password
    member_django_user.set_password(generated_password)
    # 3. update www.avonjustineithembawalkathon.co.za  password
    salt = bcrypt.gensalt()
    bcrpyt_password = bcrypt.hashpw(generated_password.encode('utf-8'), salt)
    models.Users.objects.filter(uid=walker.uid).update(password=bcrpyt_password.decode('utf-8'))
    # 4. send comm to user
    entrant_profile = models.Entrant.objects.filter(uid=walker.uid).first()
    preferred_comm_method = 'SMS' if 'sms' in entrant_profile.preferred_communication.lower() else 'EMAIL'

    if preferred_comm_method == 'SMS':
        email_to_send_to = entrant_profile.mobile + '@winsms.net'
    else:
        email_to_send_to = entrant_profile.email

    title = 'Your new iThemba Walkathon login credentials'
    message = '{}'.format(title)
    message += '\n\nHi {} {} \n'.format(entrant_profile.firstname, entrant_profile.lastname)
    message += 'You have successfully reset your password\n'
    message += 'Here are your new login credentials \n\n'
    message += 'Username: {}  \n'.format(username.lower())
    message += 'Password: {}  \n'.format(generated_password)
    send_mail(
        title,
        message,
        env.EMAIL_HOST_USER,
        [email_to_send_to],
        fail_silently=False,
    )

    return 'Password reset successful, please check your ' + preferred_comm_method.lower()
