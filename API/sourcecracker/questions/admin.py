from django.contrib import admin
from questions.models import Question, Answer, Rating


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'group')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'question')
    inlines = [RatingInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating_type', 'rate', 'answer')
