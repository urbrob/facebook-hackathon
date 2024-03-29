from django.db import models
from sourcecracker.utils import current_user
from accounts.models import Group, User
from django.urls import reverse


class Question(models.Model):
    content = models.CharField(max_length=512)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="questions", default=current_user)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} @ {self.created_at} by {self.created_by}'


class Answer(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    url = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="answers", default=current_user)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.created_by} for {self.question.content}'

    def redirect_url(self, user_hash):
        return f'http://693069ba.ngrok.io{reverse("redirect", args=[self.id, user_hash])}'

    @property
    def is_long(self):
        return self.rating_set.filter(rating_type=Rating.IS_LONG, rate=True).count() > self.rating_set.filter(rating_type=Rating.IS_LONG, rate=False).count()

    @property
    def is_complex(self):
        return self.rating_set.filter(rating_type=Rating.IS_COMPLEX, rate=True).count() > self.rating_set.filter(rating_type=Rating.IS_COMPLEX, rate=False).count()

    @property
    def is_science(self):
        return self.rating_set.filter(rating_type=Rating.IS_SCIENCE, rate=True).count() > self.rating_set.filter(rating_type=Rating.IS_SCIENCE, rate=False).count()


class Rating(models.Model):
    IS_LONG = 'is-long'
    IS_SCIENCE = 'is-science'
    IS_COMPLEX = 'is-complex'
    IS_HELPFUL = 'is-helpful'
    RATING_TYPES = (
        (IS_LONG, 'Is long'),
        (IS_SCIENCE, 'Is science'),
        (IS_COMPLEX, 'Is complex'),
        (IS_HELPFUL, 'Is helpful'),
    )
    rating_type = models.CharField(choices=RATING_TYPES, max_length=32)
    rate = models.BooleanField(default=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="ratings", default=current_user)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_by} rate {self.answer.title} as {self.rate}'


class SourceEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=current_user)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
