from graphene_django import DjangoObjectType
from accounts.models import User, Group, Membership
from sourcecracker.mixins import MutationErrorMixin
from django.db.models import Q
from django.contrib.auth import authenticate
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


class UserRegistrationMutation(MutationErrorMixin, graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    hash_id = graphene.String()

    def mutate(self, info, **kwargs):
        username = kwargs['email'].split('@')[0]
        try:
            User.objects.get(Q(username=username) | Q(email=kwargs['email']))
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=kwargs['email'], password=kwargs['password'])
            return UserRegistrationMutation(hash_id=user.hash_id)
        else:
            return UserRegistrationMutation.error('Email or username is taken')


class UserLoginMutation(MutationErrorMixin, graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    hash_id = graphene.String()

    def mutate(self, info, **kwargs):
        user = authenticate(username=kwargs['email'].split('@')[0], password=kwargs['password'])
        if user:
            return UserLoginMutation(hash_id=user.hash_id)
        else:
            return UserLoginMutation.error("Unauthorized attempt")



class Query(graphene.ObjectType):
    users = graphene.List(UserNode)

    def resolve_users(self, info):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    register_user = UserRegistrationMutation.Field()
    login_user = UserLoginMutation.Field()


schema = graphene.Schema(query=Query)
