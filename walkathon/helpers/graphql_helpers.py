import bcrypt
import newrelic.agent
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from graphql import GraphQLError

from ithemba_walkathon import env
from walkathon.models import Walker, Users, Entrant, Teams, SystemMessages
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


def send_blast_task():
    entrants = Entrant.objects.all()
    sms_recipients = []
    email_recipients = []
    for entrant in entrants:
        preferred_method = 'email' if 'email' in entrant.preferred_communication.lower() else 'sms'
        team_for_entrant = Teams.objects.filter(uid=entrant.uid).all()
        for team_member in team_for_entrant:
            print('.')
            if preferred_method == 'email':
                if team_member.email not in email_recipients:
                    # send_html_email([team_member.email])
                    email_recipients.append(team_member.email)
            else:
                mobile_email = team_member.mobile + '@winsms.net'
                if mobile_email not in sms_recipients:
                    sms_recipients.append(mobile_email)
    send_blast_sms_messages(['0760621827' + '@winsms.net'])
    send_html_email(['info@matineenterprises.com'])
    print('Done')


def send_blast_sms_messages(recipient_list):
    print('sending sms messages to recipient_list: ', recipient_list)
    title = 'Enjoy the new Walkathon App! See details below'
    message = 'Keeping abreast of cancer awareness & promoting early detection is at your fingertips through the ' \
              'iThemba Walkathon App! Download now from Play Store\App Store! '
    send_mail(
        title,
        message,
        env.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    print('done sending sms messages to recipient_list: ', recipient_list)


def send_html_email(email):
    print('sending email to : ', email)
    title = 'Enjoy the new Walkathon App! See details below'
    html_message = render_to_string('app_available_email.html')
    message = strip_tags(html_message)
    send_mail(
        title,
        message,
        env.EMAIL_HOST_USER,
        recipient_list=email,
        html_message=html_message,
        fail_silently=False,
    )
    print('done sending email to : ', email)


@newrelic.agent.function_trace()
def update_uids():
    counter = 0
    django_walkers = Walker.objects.all()
    for walker in django_walkers:
        walker_number = walker.walker_number
        print('walker_number', walker_number)
        print('counter', counter)
        team_member_profile = Teams.objects.filter(wid=int(walker_number)).first()

        if team_member_profile:
            walker.uid = int(team_member_profile.uid)
            walker.save()
        counter += 1

@newrelic.agent.function_trace()
def update_received_messages():
    system_messages_ids = SystemMessages.objects.filter(message_sent=True).values_list('pk', flat=True)
    json_list = list(system_messages_ids)
    Walker.objects.update(messages_received=json_list)
