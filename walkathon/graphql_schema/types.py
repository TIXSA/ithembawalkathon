from graphene_django import DjangoObjectType

from ..models import Walker, Walkathon, UserMessages


class WalkerType(DjangoObjectType):
    class Meta:
        model = Walker


class WalkathonType(DjangoObjectType):
    class Meta:
        model = Walkathon


class UserMessagesType(DjangoObjectType):
    class Meta:
        model = UserMessages
