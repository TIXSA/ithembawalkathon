import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Runner, Race


#1
class RunnerFilter(django_filters.FilterSet):
    class Meta:
        model = Runner
        fields = ['name', 'email', 'password']


#2
class RunnerNode(DjangoObjectType):
    class Meta:
        model = Runner
        #3
        interfaces = (graphene.relay.Node, )


class RaceNode(DjangoObjectType):
    class Meta:
        model = Race
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    #4
    relay_runner = graphene.relay.Node.Field(RunnerNode)
    #5
    relay_runners = DjangoFilterConnectionField(RunnerNode, filterset_class=RunnerFilter)


class RelayCreateRunner(graphene.relay.ClientIDMutation):
    runner = graphene.Field(RunnerNode)

    class Input:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        runner = Runner(
            name=input.get('name'),
            email=input.get('email'),
            password=input.get('password'),
            runner_profile=user
        )
        runner.save()

        return RelayCreateRunner(runner=runner)


class RelayMutation(graphene.AbstractType):
    relay_create_runner = RelayCreateRunner.Field()
