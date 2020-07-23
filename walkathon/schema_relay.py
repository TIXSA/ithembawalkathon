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
