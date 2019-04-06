import graphene
import accounts.schema
import questions.schema

class Query(accounts.schema.Query, questions.schema.Query):
    pass

class Mutation(accounts.schema.Mutation, questions.schema.Mutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
