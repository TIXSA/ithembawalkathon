import bcrypt
import newrelic.agent
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_rq import job
from graphql import GraphQLError

from ithemba_walkathon import env
from walkathon.models import Walker, Users, Entrant, Teams, SystemMessages
from .walker import get_random_alphanumeric_string, get_random_numeric_string


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

    email_to_send_to = []
    if entrant_profile.email:
        email_to_send_to.append(entrant_profile.email)
    if entrant_profile.mobile:
        email_to_send_to.append(entrant_profile.mobile + '@winsms.net')

    print('email_to_send_to', email_to_send_to)

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
        email_to_send_to,
        fail_silently=False,
    )
    return 'Password reset successful, please check your text messages and emails'


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


@job('default', timeout=10000)
def login_everyone():
    all_paid_entrants = Entrant.objects.filter(
        Q(payfast_paid='Yes') |
        Q(manual_paid='Yes')
    )
    count = 1
    for paid_entrant in all_paid_entrants:
        print('count', count)
        if not Walker.objects.filter(uid=paid_entrant.uid).exists():
            count += 1
            if count > 203:
                entrant_team_members = Teams.objects.filter(uid=paid_entrant.uid)
                print('entrant_team_members', entrant_team_members)
                for entrant_team_member in entrant_team_members:
                    emails_to_send_to = []
                    if entrant_team_member.mobile:
                        emails_to_send_to.append(entrant_team_member.mobile + '@winsms.net')
                    if entrant_team_member.email:
                        emails_to_send_to.append(entrant_team_member.email)

                    generated_username = '{}'.format(entrant_team_member.wid)
                    generated_password = get_random_numeric_string(10)
                    member_django_user = get_user_model()(
                        username=generated_username,
                        password=generated_password,
                        first_name=entrant_team_member.firstname,
                        last_name=entrant_team_member.lastname,
                    )
                    member_django_user.set_password(generated_password)
                    member_django_user.save()
                    Walker.objects.update_or_create(
                        user_profile=member_django_user,
                        defaults={
                            'uid': paid_entrant.uid,
                            'walker_number': entrant_team_member.wid,
                            'distance_to_walk': 8,
                            'team': paid_entrant.team_name,
                            'generated_username': generated_username,
                            'generated_password': generated_password,
                        }
                    )
                    send_new_login_credentials(
                        emails_to_send_to,
                        entrant_team_member.firstname,
                        generated_username,
                        generated_password
                    )


def create_app_admin():
    member_django_user = User.objects.filter(username='ithemba').first()
    member_django_user.set_password('walk')
    member_django_user.save()


def login_already_created():
    non_logged_in_walkers = Walker.objects.filter(fcm_token__isnull=True)
    count = 0
    for non_logged_in_walker in non_logged_in_walkers:
        count += 1
        if count > 20:

            print('count', count)
            print('non_logged_in_walker walker_number', non_logged_in_walker.walker_number)
            team_member_profile = Teams.objects.filter(wid=non_logged_in_walker.walker_number).first()
            if team_member_profile:
                emails_to_send_to = []

                if team_member_profile.mobile:
                    emails_to_send_to.append(team_member_profile.mobile + '@winsms.net')
                if team_member_profile.email:
                    emails_to_send_to.append(team_member_profile.email)

                generated_username = '{}'.format(team_member_profile.wid)
                generated_password = get_random_numeric_string(10)
                user = User.objects.filter(pk=non_logged_in_walker.user_profile.pk).first()

                user.username = generated_username
                user.set_password(generated_password)
                user.save()

                Walker.objects.update_or_create(
                    user_profile=user,
                    defaults={
                        'generated_username': generated_username,
                        'generated_password': generated_password,
                    }
                )
                send_new_login_credentials(
                    emails_to_send_to,
                    team_member_profile.firstname,
                    generated_username,
                    generated_password
                )


def send_new_login_credentials(emails_to_send_to, first_name, generated_username, password):
    print('sending sms messages to recipient_list: ', emails_to_send_to)
    title = 'Enjoy the new Walkathon App! See details below'
    message = 'Hi {} we have noticed that you have paid but not logged into the iThemba Walkathon App, here are your ' \
              'new login credentials. \n\nUsername: {} \nPassword: {} '.format(first_name, generated_username, password)
    send_mail(
        title,
        message,
        env.EMAIL_HOST_USER,
        recipient_list=emails_to_send_to,
        fail_silently=False,
    )
    print('done sending sms messages to recipient_list: ', emails_to_send_to)


def send_blast_task():
    team_members = Teams.objects.all()
    sms_recipients = []
    email_recipients = []
    count = 0
    for team_member in team_members:
        count += 1
        print('Count ', count)
        print('walker id ', team_member.wid)
        if count > 5821:
            if team_member.email and team_member.email not in email_recipients:
                send_html_email([team_member.email])
                # send_html_email(['info@matineenterprises.com'])
                email_recipients.append(team_member.email)

            if team_member.mobile:
                mobile_email = team_member.mobile + '@winsms.net'
                if mobile_email not in sms_recipients:
                    sms_recipients.append(mobile_email)

    send_blast_sms_messages(sms_recipients)
    # send_blast_sms_messages(['0760621827' + '@winsms.net'])

    print('Done')


def send_blast_sms_messages(recipient_list):
    print('sending sms messages to recipient_list: ', recipient_list)
    title = 'Enjoy the new Walkathon App! See details below'
    message = 'Download your new Walkathon App or update your existing App by visiting your Play Store or App Stores ' \
              'for an amazing Walkathon experience tomorrow! Tap on https://bit.ly/37UG5Ns'
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
    title = 'Start having fun with your Walkathon Mobile App!'
    html_message = render_to_string('app_updated.html')
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
