from graphene_django import DjangoObjectType
from accounts.models import User, Group, Membership
import graphene


class UserNode(DjangoObjectType):
    class Meta:
        model = User


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group


class MembershipNode(DjangoObjectType):
    class Meta:
        model = Membership


class Query(graphene.ObjectType):
    users = graphene.List(UserNode)

    def resolve_users(self, info):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
