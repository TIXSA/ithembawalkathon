import graphene
from graphql import GraphQLError

from ..models import Walker
from .types import WalkerType, StreamingType


class WalkerInput(graphene.InputObjectType):
    fcm_token = graphene.String()
    distance_to_walk = graphene.String()
    total_walked_distance = graphene.Int()
    walk_method = graphene.String()
    device_type = graphene.String()
    steps_walked = graphene.String()
    time_started = graphene.String()
    time_ended = graphene.String()
    milestones = graphene.String()
    messages_read = graphene.String()


class UpdateWalker(graphene.Mutation):
    class Arguments:
        walker_input = WalkerInput(required=True)

    walker = graphene.Field(WalkerType)

    def mutate(self, info, walker_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        Walker.objects.filter(user_profile=user_profile).update(**walker_input)
        walker = Walker.objects.filter(user_profile=user_profile).first()
        return UpdateWalker(walker)


class Mutation(graphene.ObjectType):
    update_walker = UpdateWalker.Field()
