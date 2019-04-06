from django.contrib import admin
from django.contrib import admin
from accounts.models import User, Group, Membership


class MembershipInlineAdmin(admin.TabularInline):
    model = Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display_links = ["pk"]
    list_display = ("pk", "user", "status", "group", "created_at")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display_links = ["pk"]
    list_display = ("pk", "name", "created_at", "created_by")
    inlines = [MembershipInlineAdmin]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display_links = ["pk"]
    list_display = ("pk", "first_name", "last_name", "username")
    inlines = [MembershipInlineAdmin]
