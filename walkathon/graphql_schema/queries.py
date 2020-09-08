import graphene
from graphql import GraphQLError
import json

from ..models import Walker, Walkathon, Streaming, SystemMessages
from .types import WalkerType, WalkathonType, StreamingType, MessagesType


class Query(graphene.ObjectType):
    walker = graphene.Field(WalkerType)
    walkathon = graphene.Field(WalkathonType, year=graphene.Int())
    messages = graphene.List(MessagesType)
    streams = graphene.List(StreamingType)

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
        return SystemMessages.objects.filter(pk__in=json.loads(walker.messages_received)).order_by('updated')\
            .only('title', 'message', 'image_url')
