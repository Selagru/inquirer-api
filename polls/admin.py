from django.contrib import admin
from .models import Poll, Question, Choice, Answer


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_date', 'end_date']
    inlines = [QuestionInLine]


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'question_type']
    inlines = [ChoiceInLine]
    list_filter = ('poll',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'question', 'text']
    list_filter = ('question__poll', 'question',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'lock_other']
    list_filter = ('question',)
