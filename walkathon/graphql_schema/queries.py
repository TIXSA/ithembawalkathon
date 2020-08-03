import graphene
from django.db.models import Q
from graphql import GraphQLError

from ..models import Walker, Walkathon, UserMessages
from .types import WalkerType, WalkathonType, UserMessagesType


class Query(graphene.ObjectType):
    # Add the search parameter inside our runners field
    walkers = graphene.List(
        WalkerType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    walker = graphene.Field(WalkerType)
    walkathon = graphene.Field(WalkathonType, year=graphene.Int())
    user_messages = graphene.List(UserMessagesType)

    def resolve_walkers(self, info, search=None, first=None, skip=None, **kwargs):
        walkers = Walker.objects.all()
        if search:
            filter_walker = (
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )
            walkers = walkers.filter(filter_walker)

        if skip:
            walkers = walkers[skip:]
        if first:
            walkers = walkers[:first]
        return walkers

    def resolve_walkathon(self, info, year):
        return Walkathon.objects.filter(year=year).first()

    def resolve_walker(self, info):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to get a walker profile!')
        return Walker.objects.filter(user_profile=user_profile).first()


    def resolve_user_messages(self, info, **kwargs):
        return UserMessages.objects.all()
