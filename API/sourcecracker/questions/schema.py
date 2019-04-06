from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating
import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerpNode(DjangoObjectType):
    class Meta:
        model = Answer


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question


class Query(graphene.ObjectType):
    questions = graphene.List(QuestionNode)

    def resolve_questions(self, info):
        return Question.objects.all()


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
