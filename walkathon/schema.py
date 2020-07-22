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
