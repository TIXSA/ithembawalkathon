import json

import graphene
from graphql import GraphQLError

from .types import WalkerType, WalkathonType, StreamingType, MessagesType, UserType, EntrantType, InformationType
from ..models import Walker, Walkathon, Streaming, SystemMessages, Entrant, InformationScreen


class Query(graphene.ObjectType):
    walker = graphene.Field(WalkerType)
    walkathon = graphene.Field(WalkathonType, year=graphene.Int())
    messages = graphene.List(MessagesType)
    streams = graphene.List(StreamingType)
    me = graphene.Field(UserType)
    walkers = graphene.List(WalkerType)
    entrant = graphene.Field(EntrantType)
    information = graphene.Field(InformationType)

    def resolve_information(self, info):
        return InformationScreen.objects.first()

    def resolve_entrant(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get an entrant profile!')
        walker = Walker.objects.filter(user_profile=user_profile).first()
        return Entrant.objects.filter(uid=walker.uid).first()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Not logged in')

        return user

    def resolve_streams(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get a stream!')
        return Streaming.objects.all().order_by('-pk')

    def resolve_walkathon(self, info, year):
        return Walkathon.objects.filter(year=year).first()

    def resolve_walker(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get a walker profile!')
        return Walker.objects.filter(user_profile=user_profile).first()

    def resolve_messages(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get messages!')
        walker = Walker.objects.filter(user_profile=user_profile).first()
        return SystemMessages.objects.filter(pk__in=json.loads(walker.messages_received)).order_by('-updated')

    def resolve_walkers(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get walkers!')
        walker_leader = Walker.objects.filter(user_profile=user_profile).first()
        walkers = Walker.objects.filter(uid=walker_leader.uid).exclude(user_profile=user_profile).all()
        return walkers
