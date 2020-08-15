import graphene
from graphql import GraphQLError
from django.forms.models import model_to_dict

from ithemba_walkathon.graphql_schema.types import UserType
from ..models import Walker, Walkathon, UserMessages
from .types import WalkerType, UserMessagesType


# 1 mutation class
class CreateWalker(graphene.Mutation):
    # output of the mutation
    id = graphene.Int()
    walker_number = graphene.String()
    user_profile = graphene.Field(UserType)

    # 2 data you can send to the server
    class Arguments:
        walker_number = graphene.String()

    # 3 mutation method: it creates a Runner in the database using the data sent by the user
    def mutate(self, info, walker_number):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        walker = Walker(walker_number=walker_number, user_profile=user_profile)
        walker.save()

        # server returns the CreateRunner class with the data just created
        return CreateWalker(
            id=walker.id,
            walker_number=walker.walker_number,
            user_profile=walker.user_profile,
        )


class WalkerInput(graphene.InputObjectType):
    walker_number = graphene.String()
    fcm_token = graphene.String()
    distance_to_walk = graphene.String()
    total_walked_distance = graphene.Int()
    walk_method = graphene.String()
    device_type = graphene.String()
    steps_walked = graphene.String()
    time_started = graphene.String()
    time_ended = graphene.String()
    milestones = graphene.String()


class CreateOrUpdateWalker(graphene.Mutation):
    class Arguments:
        walker_input = WalkerInput(required=True)

    walker = graphene.Field(WalkerType)

    def mutate(self, info, walker_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        walker, created = Walker.objects.update_or_create(user_profile=user_profile, defaults={**walker_input})
        return CreateOrUpdateWalker(walker)


class UserMessageInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    message_opened = graphene.Boolean(required=True)


class UpdateUserMessage(graphene.Mutation):
    user_message = graphene.Field(UserMessagesType)

    class Arguments:
        user_message_input = UserMessageInput(required=True)

    def mutate(self, info, user_message_input):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        UserMessages.objects.filter(
            user_profile=user_profile,
            pk=user_message_input.id).update(**user_message_input)
        user_message = UserMessages.objects.filter(user_profile=user_profile, pk=user_message_input.id).first()

        return UpdateUserMessage(user_message)


class CreateWalkathon(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    year = graphene.String()
    starting_time = graphene.String()
    created_by = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        year = graphene.String()
        starting_time = graphene.String()

    def mutate(self, info, name, year, starting_time):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a new walkathon')

        new_walkathon = Walkathon.objects.create(
            name=name,
            year=year,
            starting_time=starting_time,
            created_by=user_profile
        )

        new_walkathon.save()

        return CreateWalkathon(
            name=new_walkathon.name,
            year=new_walkathon.year,
            starting_time=new_walkathon.starting_time,
            created_by=new_walkathon.user_profile
        )


class Mutation(graphene.ObjectType):
    create_walker = CreateWalker.Field()
    create_walkathon = CreateWalkathon.Field()
    create_or_update_walker = CreateOrUpdateWalker.Field()
    update_user_message = UpdateUserMessage.Field()
