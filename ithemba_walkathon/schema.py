import graphene

import walkathon.schema


class Query(walkathon.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
