import graphene
from graphene.types.generic import GenericScalar


class ErrorType(graphene.ObjectType):
    message = graphene.String()
    fields = GenericScalar()
