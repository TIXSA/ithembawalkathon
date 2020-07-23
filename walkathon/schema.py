import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Runner, Race
from ithemba_walkathon.users.schema import UserType


class RunnerType(DjangoObjectType):
    class Meta:
        model = Runner


class RaceType(DjangoObjectType):
    class Meta:
        model = Race


class Query(graphene.ObjectType):
    runners = graphene.List(RunnerType)
    races = graphene.List(RaceType)

    def resolve_runners(self, info, **kwargs):
        return Runner.objects.all()

    def resolve_races(self, info, **kwargs):
        return Race.objects.all()


# 1 mutation class
class CreateRunner(graphene.Mutation):
    # output of the mutation
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    runner_profile = graphene.Field(UserType)

    # 2 data you can send to the server
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    # 3 mutation method: it creates a Runner in the database using the data sent by the user
    def mutate(self, info, name, email, password):
        runner_profile = info.context.user or None
        runner = Runner(name=name, email=email, password=password, runner_profile=runner_profile)
        runner.save()

        # server returns the CreateRunner class with the data just created
        return CreateRunner(
            id=runner.id,
            name=runner.name,
            email=runner.email,
            runner_profile=runner.runner_profile
        )


class CreateRace(graphene.Mutation):
    runner_profile = graphene.Field(UserType)
    runner = graphene.Field(RunnerType)
    distance = graphene.String()

    class Arguments:
        runner_id = graphene.Int()

    def mutate(self, info, runner_id):
        runner_profile = info.context.user
        if runner_profile.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        runner = Runner.objects.filter(id=runner_id).first()
        if not runner:
            raise Exception('Invalid runner')

        new_race = Race.objects.create(
            runner_profile=runner_profile,
            runner=runner
        )

        return CreateRace(
            runner_profile=runner_profile,
            runner=runner,
            distance=new_race.distance
        )


# 4 Creates a mutation class with a field to be resolved, which points to our CreateRunner mutation
class Mutation(graphene.ObjectType):
    create_runner = CreateRunner.Field()
    create_race = CreateRace.Field()
