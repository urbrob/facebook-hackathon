from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating, SourceEntry
from graphene import Argument, Boolean, String, Int
from accounts.models import User
from accounts.schema import UserNode
import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerNode(DjangoObjectType):
    url = String(user_hash=Argument(String))
    is_visited = Boolean(user_hash=Argument(String, required=True))

    class Meta:
        model = Answer
        only_fields = ('id', 'title', 'url', 'created_by', 'created_at', 'is_long', 'is_complex', 'is_science', 'is_visited')

    def resolve_is_long(self, info):
        return self.is_long

    def resolve_is_complex(self, info):
        return self.is_complex

    def resolve_url(self, info, **kwargs):
        try:
            return self.redirect_url(kwargs['user_hash'])
        except KeyError:
            return self.url

    def resolve_is_visited(self, info, **kwargs):
        return SourceEntry.objects.filter(user__hash_id=kwargs['user_hash'], answer=self)

    def resolve_is_science(self, info):
        return self.is_science

    def resolve_created_by(self, info):
        return self.created_by


class QuestionNode(DjangoObjectType):
    answers = graphene.List(AnswerNode, is_long=Argument(Boolean),
                            is_science=Argument(Boolean), is_complex=Argument(Boolean),
                            user=Argument(String))

    class Meta:
        model = Question

    def resolve_answers(self, info, *args, **kwargs):
        answers = self.answer_set.all()
        for key, value in kwargs.items():
            answers = filter(lambda x: getattr(x, key) == value, answers)
        return answers


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


class RatingTypes(graphene.Enum):
    IS_LONG = Rating.IS_LONG
    IS_SCIENCE = Rating.IS_SCIENCE
    IS_COMPLEX = Rating.IS_COMPLEX
    IS_HELPFUL = Rating.IS_HELPFUL


class CreateRating(graphene.Mutation):
    class Arguments:
        rate = graphene.Boolean(required=True)
        hash_id = graphene.String(required=True)
        answer_id = graphene.Int(required=True)
        rating_type = RatingTypes()

    rating = graphene.Field(RatingNode)

    def mutate(self, info, *arg, **kwargs):
        user = User.objects.get(hash_id=kwargs['hash_id'])
        answer = Answer.objects.get(id=kwargs['answer_id'])
        rating = Rating.objects.create(answer=answer, created_by=user, rate=kwargs['rate'], rating_type=kwargs['rating_type'])
        return CreateRating(rating=rating)


class CreateAnswer(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        question_id = graphene.Int(required=True)
        hash_id = graphene.String(required=True)

    answer = graphene.Field(AnswerNode)

    def mutate(self, info, *arg, **kwargs):
        user = User.objects.get(hash_id=kwargs['hash_id'])
        question = Question.objects.get(id=kwargs['question_id'])
        sender_email = question.created_by.email
        answer = Answer.objects.create(title=kwargs['title'], url=kwargs['url'], question=question, created_by=user)

        return CreateAnswer(answer=answer)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_rating = CreateRating.Field()
    create_answer = CreateAnswer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
