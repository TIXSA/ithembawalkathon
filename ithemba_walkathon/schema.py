import graphene
import graphql_jwt

from walkathon.graphql_schema.queries import Query as WalkathonQuery
from walkathon.graphql_schema.mutations import Mutation as WalkathonMutation


class Query(WalkathonQuery, graphene.ObjectType):
    pass


class Mutation(WalkathonMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
