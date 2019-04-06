from django.shortcuts import render
from questions.models import Answer, SourceEntry
from django.http import Http404
from django.shortcuts import redirect
from accounts.models import User


def redirect_counter(request, answer_id, user_hash):
    try:
        answer = Answer.objects.get(id=answer_id)
    except Question.DoesNotExist:
        return Http404('Question does not exists')
    try:
        user = User.objects.get(hash_id=user_hash)
    except User.DoesNotExist:
        return Http404('User does not exists')
    SourceEntry.objects.get_or_create(answer=answer, user=user)
    return redirect(answer.url)
