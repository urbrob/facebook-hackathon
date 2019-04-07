from graphene_django import DjangoObjectType
from questions.models import Question, Answer, Rating, SourceEntry
from graphene import Argument, Boolean, String, Int
from accounts.models import User
from accounts.schema import UserNode
from django.core.mail import send_mail
from django.db.models import Q

import graphene


class RatingNode(DjangoObjectType):
    class Meta:
        model = Rating


class AnswerNode(DjangoObjectType):
    url = String(user_hash=Argument(String))
    is_visited = Boolean(user_hash=Argument(String, required=True))
    is_long = String()
    is_complex = String()
    is_science = String()

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
    answers_count = graphene.Int()

    class Meta:
        model = Question

    def resolve_answers(self, info, *args, **kwargs):
        answers = self.answer_set.all()
        for key, value in kwargs.items():
            answers = filter(lambda x: getattr(x, key) == value, answers)
        return answers

    def resolve_answers_count(self, info):
        return self.answer_set.count()


class Query(graphene.ObjectType):
    questions = graphene.List(
        QuestionNode,
        question=Argument(String)
    )
    question = graphene.Field(
        QuestionNode,
        question_id=Argument(Int, required=True)
    )
    user_questions = graphene.List(
        QuestionNode,
        hash_id=Argument(String, required=True)
    )

    def resolve_question(self, info, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def resolve_questions(self, info, **kwargs):
        return Question.objects.filter(content__icontains=kwargs.get('question', ''))

    def resolve_user_questions(self, info, **kwargs):
        return Question.objects.filter(created_by__hash_id=kwargs['hash_id'])


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
        try:
            rating = Rating.objects.create(answer=answer, created_by=user, rating_type=kwargs['rating_type'])
            rating.rate = kwargs['rate']
            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(answer=answer, created_by=user, rate=kwargs['rate'], rating_type=kwargs['rating_type'])
        return CreateRating(rating=rating)


class CreateAnswer(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        question_id = graphene.Int(required=True)
        hash_id = graphene.String(required=True)
        is_long = graphene.Boolean(required=True)
        is_complex = graphene.Boolean(required=True)
        is_science = graphene.Boolean(required=True)

    answer = graphene.Field(AnswerNode)

    def mutate(self, info, *arg, **kwargs):
        user = User.objects.get(hash_id=kwargs.pop('hash_id'))
        question = Question.objects.get(id=kwargs.pop('question_id'))
        sender_email = question.created_by.email
        answer = Answer.objects.create(title=kwargs.pop('title'), url=kwargs.pop('url'), question=question, created_by=user)
        for key, value in kwargs.items():
            key = key.replace('_', '-')
            Rating.objects.create(rating_type=key, rate=value, answer=answer, created_by=user)
        return CreateAnswer(answer=answer)


class BroadcastHelpEmail(graphene.Mutation):
    class Arguments:
        hash_id = graphene.String(required=True)
        question_id = graphene.Int(required=True)

    status = graphene.String()

    def mutate(self, info, *arg, **kwargs):
        question = Question.objects.get(id=kwargs['question_id'])
        emails = User.objects.filter(~Q(hash_id=question.created_by.hash_id)).values_list('email', flat=True)
        #import pdb; pdb.set_trace()
        send_mail(
            'Please, help !!',
            f'Hello, please, we need your help with answering this question: {question.id}',
            'adka94@op.pl',
            [emails],
            fail_silently=False,
            )

        return BroadcastHelpEmail(status="That is perfect!")


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_rating = CreateRating.Field()
    create_answer = CreateAnswer.Field()
    broadcast_help_email = BroadcastHelpEmail.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
