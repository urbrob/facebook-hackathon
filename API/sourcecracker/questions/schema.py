from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating
from accounts.models import User
import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerNode(DjangoObjectType):
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


class RatingTypes(graphene.Enum):
    IS_LONG = Rating.IS_LONG
    IS_SCIENCE = Rating.IS_SCIENCE
    IS_COMPLEX = Rating.IS_COMPLEX


class CreateRating(graphene.Mutation):
    class Arguments:
        rate = graphene.Boolean(required=True)
        hash_id = graphene.String(required=True)
        answer_id = graphene.Int(required=True)
        rating_type = RatingTypes()

    rating = graphene.Field(RatingNode)

    def mutate(self, info, *arg, **kwargs):
        user = User.objects.get(hash_id=kwargs['hash_id'])
        answer = Answer.objects.get(answer_id=kwargs['answer_id'])
        rating_type = Ra
        rating = Rating.objects.create(answer=answer, created_by=user, rate=kwargs['rate'], rating_type=Rating.IS_LONG)
        return CreateRating(rating=rating)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_rating = CreateRating.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
