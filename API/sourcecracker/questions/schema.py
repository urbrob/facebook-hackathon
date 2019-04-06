from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating
from accounts.models import User
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
