from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from questions.models import Answer


@receiver(post_save, sender=Answer)
def send_notification(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        sender_mail = question.created_by.email
        send_mail(
            'You\'ve got your answer!!',
            f'Hello, please, check your new answer: {instance.redirect_url(question.created_by.hash_id)}, a new answer is awaiting',
            'adka94@op.pl',
            [sender_mail],
            fail_silently=False,
        )
