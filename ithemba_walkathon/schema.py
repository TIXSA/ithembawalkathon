import graphene
import graphql_jwt

from walkathon.graphql_schema.queries import Query as WalkathonQuery
from walkathon.graphql_schema.mutations import Mutation as WalkathonMutation
from ithemba_walkathon.users.schema import Mutation as UsersMutation, Query as UsersQuery


class Query(WalkathonQuery, UsersQuery, graphene.ObjectType):
    pass


class Mutation(WalkathonMutation, UsersMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
