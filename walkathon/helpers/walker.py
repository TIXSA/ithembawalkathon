from django.contrib.auth import get_user_model
from graphql import GraphQLError


def create_new_user(username, password):
    check_if_user_in_users_table()
    user = get_user_model()(
        username=username,
        password=password,
    )
    user.set_password(password)
    user.save()

    return user


def check_if_user_in_users_table():
    raise GraphQLError('Enter valid balsllslsa and password')