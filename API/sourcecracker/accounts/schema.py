from graphene_django import DjangoObjectType
from accounts.models import User, Group, Membership
from sourcecracker.mixins import MutationErrorMixin
from django.db.models import Q
from django.contrib.auth import authenticate
from django.core.mail import send_mail
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


class StatusEnum(graphene.Enum):
    OWNER = Membership.OWNER
    MODERATOR = Membership.MODERATOR
    USER = Membership.USER


class AddGroup(graphene.Mutation):
    class Arguments:
        hash_id = graphene.String(required=True)
        group = graphene.String(required=True)

    group = graphene.Field(GroupNode)

    def mutate(self, info, **kwargs):
        user = User.objects.get(hash_id=kwargs['hash_id'])
        group = Group.objects.create(name=kwargs['group'], created_by=user)
        Membership.objects.create(user=user, group=group, status=Membership.OWNER)
        return AddGroup(group=group)


class AddToGroup(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        group_id = graphene.Int(required=True)

    status = graphene.Boolean()

    def mutate(self, info, **kwargs):
        user = User.objects.get(email=kwargs['email'])
        group = Group.objects.get(id=kwargs['group_id'])
        send_mail(
            'Welcome to new group!!',
            f'Hello, someone invite you to new group. Please click on link in order to join!\n{group.invite_user(user.hash_id)}',
            'adka94@op.pl',
            [user.email],
            fail_silently=True,
        )
        return AddToGroup(status=True)


class UserLoginMutation(MutationErrorMixin, graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    hash_id = graphene.String()
    in_group = graphene.Boolean()

    def mutate(self, info, **kwargs):
        user = authenticate(username=kwargs['email'].split('@')[0], password=kwargs['password'])
        if user:
            return UserLoginMutation(hash_id=user.hash_id, in_group=user.group_memberships.exists())
        else:
            return UserLoginMutation.error("Unauthorized attempt")



class Query(graphene.ObjectType):
    users = graphene.List(UserNode)
    user_groups = graphene.List(
        GroupNode,
        hash_id=graphene.Argument(graphene.String, required=True)
    )

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user_groups(self, info, **kwargs):
        return Group.objects.filter(memberships__user__hash_id=kwargs['hash_id'])


class Mutation(graphene.ObjectType):
    register_user = UserRegistrationMutation.Field()
    login_user = UserLoginMutation.Field()
    add_to_group = AddToGroup.Field()
    add_group = AddGroup.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
