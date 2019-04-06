from django.db import models
from django.contrib.auth.models import AbstractUser
from sourcecracker.utils import current_user

# Create your models here.


class User(AbstractUser):
    pass


class Group(models.Model):
    name = models.CharField(max_length=250)
    users = models.ManyToManyField(User, through="accounts.Membership")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="created_groups", default=current_user)


class Membership(models.Model):
    OWNER = "owner"
    MODERATOR = "moderator"
    USER = "user"
    STATUSES = ((OWNER, "Owner"), (MODERATOR, "Moderator"), (USER, "User"))

    status = models.CharField(choices=STATUSES, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    created_at = models.DateTimeField(auto_now_add=True)
