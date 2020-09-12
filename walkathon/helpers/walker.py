import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from walkathon.models import Users, Entrant
from graphql import GraphQLError

errors = {
    '0': 'Create walker error',
    '1': 'You must first add a participant profile at www.ithembawalkathon.co.za',
    '2': 'The amount paid is not equal to the total owed amount for all registered member(s)',
    '3': 'The amount paid via PayFast is not equal to the total owed amount for all registered member(s)',
    '4': 'The amount paid manually is not equal to the total owed amount for all registered member(s)',
    '5': 'If you have completed your registration, please make sure you have made a manual or '
         'PayFast payment.',
    '6': 'Invalid login credentials',
    '7': 'Invalid username',
    '8': 'Password and username do not match',
}


class WalkerHelper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.php_user = None
        self.django_user = None
        self.php_user_uid = 0
        self.entrant = None

    def create_new_walker(self):
        self.check_if_user_in_users_table()
        self.check_if_input_password_same_as_user_password()
        self.check_if_entrant_paid()
        self.add_leader_walker_profile()

        raise GraphQLError(errors['0'])

    def add_leader_walker_profile(self):
        self.django_user.first_name = self.entrant.firstname
        self.django_user.last_name = self.entrant.lastname
        self.django_user.save()

    def check_if_entrant_paid(self):
        entrant = Entrant.objects.filter(uid=self.php_user_uid).first()

        if not entrant:
            raise GraphQLError(errors['1'])
        elif entrant.payfast_paid == 'Yes' and entrant.manual_paid == 'Yes':
            if entrant.total_amount == entrant.manual_paid_amount + entrant.payfast_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(errors['2'])

        elif entrant.payfast_paid == 'Yes' and not entrant.manual_paid:
            if entrant.total_amount == entrant.payfast_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(errors['3'])
        elif entrant.manual_paid == 'Yes' and not entrant.payfast_paid:
            if entrant.total_amount == entrant.manual_paid_amount:
                self.new_auth_user()
                self.entrant = entrant
            else:
                raise GraphQLError(errors['4'])
        else:
            raise GraphQLError(errors['5'])

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
            raise GraphQLError(errors['6'])

        user = Users.objects.filter(username=self.username).first()
        if user:
            self.php_user = user
        else:
            raise GraphQLError(errors['7'])

    def check_if_input_password_same_as_user_password(self):
        if self.php_user.password.find('$2y$10$') == 0:
            passwords_match = bcrypt.checkpw(self.password.encode('utf-8'), self.php_user.password.encode('utf-8'))
        else:
            passwords_match = self.password == self.php_user.password

        if not passwords_match:
            raise GraphQLError(errors['8'])

        if self.php_user.long_uid > 0:
            self.php_user_uid = self.php_user.long_uid
        else:
            self.php_user_uid = self.php_user.uid
