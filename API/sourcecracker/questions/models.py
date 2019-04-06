from django.db import models
from sourcecracker.utils import current_user
from accounts.models import Group, User


class Question(models.Model):
    content = models.CharField(max_length=512)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Answer(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Rating(models.Model):
    IS_LONG = 'is-long'
    IS_SCIENCE = 'is-science'
    IS_COMPLEX = 'is-complex'
    RATING_TYPES = (
        (IS_LONG, 'Is long'),
        (IS_SCIENCE, 'Is science'),
        (IS_COMPLEX, 'Is complex'),
    )
    rating_type = models.CharField(choices=RATING_TYPES, max_length=32)
    rate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
