import graphene
from graphql import GraphQLError

from ithemba_walkathon.graphql_schema.types import UserType
from ..models import Walker, Walkathon, UserMessages
from .types import WalkerType


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


# 1 mutation class
class UpdateWalker(graphene.Mutation):
    # output of the mutation
    walker = graphene.Field(WalkerType)

    # 2 data you can send to the server
    class Arguments:
        field_name = graphene.String()
        field_value = graphene.String()

    # 3 mutation method: it creates a Runner in the database using the data sent by the user
    def mutate(self, info, field_name, field_value):
        user_profile = info.context.user
        if user_profile.is_anonymous:
            raise GraphQLError('You must be logged to create a walker profile!')
        walker = Walker.objects.filter(user_profile=user_profile).first()
        walker.distance_to_walk = 8
        walker.save()
        print('what came innnnkn\n')
        print(field_name)
        print(field_value)
        print(walker)
        print('=======================\n')

        # server returns the CreateRunner class with the data just created
        return Walker.objects.filter(user_profile=user_profile).first()


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


# 4 Creates a mutation class with a field to be resolved, which points to our CreateRunner mutation
class Mutation(graphene.ObjectType):
    create_walker = CreateWalker.Field()
    create_walkathon = CreateWalkathon.Field()
    update_walker = UpdateWalker.Field()
