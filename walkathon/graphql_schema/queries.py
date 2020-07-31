import graphene
from django.db.models import Q

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
    walkathon = graphene.List(WalkathonType)
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

    def resolve_walkathons(self, info, **kwargs):
        return Walkathon.objects.all()

    def resolve_user_messages(self, info, **kwargs):
        return UserMessages.objects.all()
