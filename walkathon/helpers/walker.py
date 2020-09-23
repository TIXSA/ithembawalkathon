import random
import string

import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphql import GraphQLError

from ithemba_walkathon import env
from walkathon.models import Walker, Entrant, Teams, Users


class WalkerHelper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.php_user = None
        self.django_user = None
        self.php_user_uid = 0
        self.entrant = None
        self.team = None

    def create_new_walker(self):
        self.check_if_user_in_users_table()
        self.check_if_input_password_same_as_user_password()
        self.check_if_entrant_paid()
        self.get_team_members()
        return self.django_user

    def get_team_members(self):
        team = Teams.objects.filter(uid=self.php_user_uid).order_by('wid')
        if team:
            for index, member in enumerate(team):
                if index == 0:
                    self.add_leader_walker_profile(member.wid)
                else:
                    self.add_member_walker_profile(member)
        else:
            User.objects.filter(username=self.username).delete()
            raise GraphQLError(env.ERRORS['9'])

    def add_member_walker_profile(self, member):
        generated_username = '{}_{}_{}'.format(member.wid, member.firstname, member.lastname)
        generated_password = get_random_alphanumeric_string(10)
        member_django_user = get_user_model()(
            username=generated_username,
            password=generated_password,
            first_name=member.firstname,
            last_name=member.lastname,
        )
        member_django_user.set_password(generated_password)
        member_django_user.save()
        Walker.objects.update_or_create(
            user_profile=member_django_user,
            defaults={
                'uid': self.php_user_uid,
                'walker_number': member.wid,
                'distance_to_walk': 8,
                'team': member.team_name,
                'generated_username': generated_username,
                'generated_password': generated_password,
            }
        )

    def add_leader_walker_profile(self, walker_number):
        self.django_user.first_name = self.entrant.firstname
        self.django_user.last_name = self.entrant.lastname
        self.django_user.save()
        Walker.objects.update_or_create(
            user_profile=self.django_user,
            defaults={
                'uid': self.php_user_uid,
                'walker_number': walker_number,
                'distance_to_walk': 8 if self.entrant.walk_distance == '8km' else 4,
                'team': self.entrant.team_name,
                'walker_leader': True,
            }
        )

    def check_if_entrant_paid(self):
        entrant = Entrant.objects.filter(uid=self.php_user_uid).first()

        if not entrant:
            raise GraphQLError(env.ERRORS['1'])
        elif entrant.payfast_paid == 'Yes' and entrant.manual_paid == 'Yes':
            if entrant.total_amount == entrant.manual_paid_amount + entrant.payfast_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(env.ERRORS['2'])

        elif entrant.payfast_paid == 'Yes':
            if entrant.total_amount == entrant.payfast_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(env.ERRORS['3'])
        elif entrant.manual_paid == 'Yes':
            if entrant.total_amount == entrant.manual_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(env.ERRORS['4'])
        else:
            raise GraphQLError(env.ERRORS['5'])

    def new_auth_user(self):
        user = get_user_model()(
            username=self.username,
            password=self.password,
        )
        user.set_password(self.password)
        self.django_user = user
        user.save()

    def check_if_user_in_users_table(self):
        django_user = User.objects.filter(username=self.username).first()
        if django_user:
            raise GraphQLError(env.ERRORS['6'])

        user = Users.objects.filter(username=self.username).first()
        if user:
            self.php_user = user
        else:
            raise GraphQLError(env.ERRORS['7'])

    def check_if_input_password_same_as_user_password(self):
        if self.php_user.password.find('$2y$10$') == 0 or self.php_user.password.find('$2b$12$') == 0:
            passwords_match = bcrypt.checkpw(self.password.encode('utf-8'), self.php_user.password.encode('utf-8'))
        else:
            passwords_match = self.password == self.php_user.password

        if not passwords_match:
            raise GraphQLError(env.ERRORS['8'])

        if self.php_user.long_uid > 0:
            self.php_user_uid = self.php_user.long_uid
        else:
            self.php_user_uid = self.php_user.uid


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))
