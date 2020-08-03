from django.contrib import admin
from .models import Poll, Question, SingleChoice, MultipleChoice, Answer


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'max_points']
    inlines = [QuestionInLine]


class SingleChoiceInLine(admin.TabularInline):
    model = SingleChoice
    extra = 3


class MultipleChoiceInLine(admin.TabularInline):
    model = MultipleChoice
    extra = 3


@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_type', 'total_points']
    inlines = [SingleChoiceInLine, MultipleChoiceInLine]
    list_filter = ('poll', 'question_type',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'question', 'text', 'earned_points']
    list_filter = ('question__poll', 'question', 'user', 'session_key')


@admin.register(SingleChoice)
class SingleChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'question', 'points']
    list_filter = ('question__poll', 'question')


@admin.register(MultipleChoice)
class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'question', 'points']
    list_filter = ('question__poll', 'question')
