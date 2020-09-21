import bcrypt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from graphql import GraphQLError

from ithemba_walkathon import env
from walkathon.models import Walker, Users, Entrant
from .walker import get_random_alphanumeric_string


def send_password_reset_message(username):
    if not username or not User.objects.filter(username=username).exists():
        raise GraphQLError(env.ERRORS['7'])

    member_django_user = User.objects.filter(username=username).first()
    walker = Walker.objects.filter(user_profile=member_django_user).first()
    if not walker.walker_leader:
        raise GraphQLError(env.ERRORS['10'])

    # 1. Generate new password
    generated_password = get_random_alphanumeric_string(10)
    # 2. Update django password
    member_django_user.set_password(generated_password)
    member_django_user.save()
    # 3. update www.avonjustineithembawalkathon.co.za  password
    salt = bcrypt.gensalt()
    bcrpyt_password = bcrypt.hashpw(generated_password.encode('utf-8'), salt)
    Users.objects.filter(uid=walker.uid).update(password=bcrpyt_password.decode('utf-8'))
    # 4. send comm to user
    entrant_profile = Entrant.objects.filter(uid=walker.uid).first()
    preferred_comm_method = 'text messages' if 'sms' in entrant_profile.preferred_communication.lower() else 'emails'

    if preferred_comm_method == 'emails':
        email_to_send_to = entrant_profile.email
    else:
        email_to_send_to = entrant_profile.mobile + '@winsms.net'

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

    return 'Password reset successful, please check your ' + preferred_comm_method


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
