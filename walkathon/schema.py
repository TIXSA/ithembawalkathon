import graphene
from graphene_django import DjangoObjectType

from .models import Runner


class RunnerType(DjangoObjectType):
    class Meta:
        model = Runner


class Query(graphene.ObjectType):
    runners = graphene.List(RunnerType)

    def resolve_runners(self, info, **kwargs):
        return Runner.objects.all()


# 1 mutation class
class CreateRunner(graphene.Mutation):
    # output of the mutation
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()

    # 2 data you can send to the server
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    # 3 mutation method: it creates a Runner in the database using the data sent by the user
    def mutate(self, info, name, email, password):
        runner = Runner(name=name, email=email, password=password)
        runner.save()

        # server returns the CreateRunner class with the data just created
        return CreateRunner(
            id=runner.id,
            name=runner.name,
            email=runner.email
        )


# 4 Creates a mutation class with a field to be resolved, which points to our CreateRunner mutation
class Mutation(graphene.ObjectType):
    create_runner = CreateRunner.Field()
