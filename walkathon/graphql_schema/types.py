from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
from ..models import Walker, Walkathon, SystemMessages, Streaming, Entrant, InformationScreen


class InformationType(DjangoObjectType):
    class Meta:
        model = InformationScreen


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class EntrantType(DjangoObjectType):
    class Meta:
        model = Entrant


class WalkerType(DjangoObjectType):
    class Meta:
        model = Walker


class WalkathonType(DjangoObjectType):
    class Meta:
        model = Walkathon


class MessagesType(DjangoObjectType):
    class Meta:
        model = SystemMessages


class StreamingType(DjangoObjectType):
    class Meta:
        model = Streaming
