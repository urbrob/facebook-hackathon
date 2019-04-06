from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating
from graphene import Argument, Boolean, String, Int
from django.db.models import Subquery, Count
from accounts.models import User
from accounts.schema import UserNode
import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerNode(DjangoObjectType):
    created_by = graphene.Field(UserNode)
    is_long = graphene.Boolean()
    is_complex = graphene.Boolean()
    is_science = graphene.Boolean()

    class Meta:
        model = Answer
        only_fields = ('id', 'title', 'url', 'created_by', 'created_at', 'is_long', 'is_complex', 'is_science')

    def resolve_is_long(self, info):
        return self.is_long

    def resolve_is_complex(self, info):
        return self.is_complex

    def resolve_is_science(self, info):
        return self.is_science

    def resolve_created_by(self, info):
        return self.created_by


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
    question = graphene.Field(
        QuestionNode,
        question_id=Argument(Int, required=True)
    )

    def resolve_question(self, info, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def resolve_questions(self, info, **kwargs):
        return Question.objects.filter(content__icontains=kwargs.get('question', ''))


class CreateQuestion(graphene.Mutation):
    class Arguments:
        question = graphene.String(required=True)
        hash_id = graphene.String(required=True)

    question = graphene.Field(QuestionNode)

    def mutate(self, info, *arg, **kwargs):
        user = User.objects.get(hash_id=kwargs['hash_id'])
        question = Question.objects.create(content=kwargs['question'], created_by=user)
        return CreateQuestion(question=question)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
