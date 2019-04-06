from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating
from graphene import Argument, Boolean, String
from django.db.models import Subquery, Count
import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer


class QuestionNode(DjangoObjectType):
    answers = graphene.List(AnswerNode, is_long=Argument(Boolean), is_science=Argument(Boolean), is_complex=Argument(Boolean))

    class Meta:
        model = Question

    def resolve_answers(self, info, *args, **kwargs):
        return self.answer_set.all()


class Query(graphene.ObjectType):
    questions = graphene.List(
        QuestionNode,
        question=Argument(String)
    )

    def resolve_questions(self, info, **kwargs):
        return Question.objects.filter(content__icontains=kwargs.get('question', ''))


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
