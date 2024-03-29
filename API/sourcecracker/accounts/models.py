from django.db import models
from django.contrib.auth.models import AbstractUser
from sourcecracker.utils import current_user
from django.shortcuts import redirect
from django.urls import reverse
import uuid


class User(AbstractUser):
    hash_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Group(models.Model):
    name = models.CharField(max_length=250)
    users = models.ManyToManyField(User, through="accounts.Membership")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="created_groups", default=current_user)

    def invite_user(self, user_hash):
        return f'http://693069ba.ngrok.io{reverse("invite", args=[user_hash, self.id])}'


class Membership(models.Model):
    OWNER = "owner"
    MODERATOR = "moderator"
    USER = "user"
    STATUSES = ((OWNER, "Owner"), (MODERATOR, "Moderator"), (USER, "User"))

    status = models.CharField(choices=STATUSES, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    created_at = models.DateTimeField(auto_now_add=True)
