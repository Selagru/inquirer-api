from django.db import models
from django.conf import settings
from django.db.models import Sum


class Poll(models.Model):
    name = models.CharField(max_length=255, help_text='Название опроса')
    start_date = models.DateTimeField(auto_now_add=True, editable=False, help_text='Дата старта')
    end_date = models.DateTimeField(null=True, blank=True, help_text='Дата окончания')
    description = models.TextField(help_text='Описание опроса')

    class Meta:
        ordering = ['start_date']

    def max_points(self):
        total_1 = self.question_set.filter(question_type='single').aggregate(total=Sum('singlechoice__points'))['total']
        total_2 = self.question_set.filter(question_type='multiple').aggregate(total=Sum('multiplechoice__points'))['total']
        if total_1 is None:
            total_1 = 0
        if total_2 is None:
            total_2 = 0

        return total_1 + total_2

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):

    QUESTION_TYPE = (
        ('text', 'ответ текстом'),
        ('single', 'ответ с выбором одного варианта'),
        ('multiple', 'ответ с выбором нескольких вариантов'),
    )

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    text = models.CharField(max_length=4096, help_text='Текст вопроса')
    question_type = models.CharField(max_length=8, choices=QUESTION_TYPE, default='text', help_text='Тип вопроса')

    class Meta:
        ordering = ['id']

    def total_points(self):
        total_for_single_choices = self.singlechoice_set.aggregate(total=Sum('points'))['total']
        total_for_multiple_choices = self.multiplechoice_set.aggregate(total=Sum('points'))['total']
        if total_for_single_choices is None:
            total_for_single_choices = 0
        if total_for_multiple_choices is None:
            total_for_multiple_choices = 0
        return total_for_single_choices + total_for_multiple_choices

    def __str__(self):
        return f'{self.text} / Type: {self.question_type}'


class SingleChoice(models.Model):
    title = models.CharField(max_length=4096, help_text='Текст выбора')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(help_text='Очков за выбор этого ответа')

    def is_correct(self):
        if self.points == 0:
            return False
        return True

    def lock_other(self):
        return True

    def __str__(self):
        return self.title


class MultipleChoice(models.Model):
    title = models.CharField(max_length=4096, help_text='Текст выбора')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(help_text='Очков за выбор этого ответа')

    def is_correct(self):
        if self.points == 0:
            return False
        return True

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING)
    session_key = models.CharField(max_length=32, help_text='уникальный ключ браузерной сессии пользователя')
    single_choice = models.ForeignKey('SingleChoice', null=True, blank=True, on_delete=models.DO_NOTHING)
    multiple_choice = models.ManyToManyField('MultipleChoice', blank=True)
    text = models.TextField(null=True, blank=True, help_text='Текстовый ответ пользователя')
    created = models.DateTimeField(auto_now_add=True, editable=False, help_text='Дата и время ответа')

    def is_text(self):
        if self.question.question_type == 'text':
            return True
        return False

    def is_one_choice(self):
        if self.question.question_type == 'single':
            return True
        return False

    def is_multiple_choices(self):
        if self.question.question_type == 'multiple':
            return True
        return False

    def earned_points(self):
        if self.single_choice is None:
            total1 = 0
        else:
            total1 = self.single_choice.points
        total2 = self.multiple_choice.aggregate(total=Sum('points'))['total']
        if total2 is None:
            total2 = 0
        return total1 + total2

    def __str__(self):
        return f'Ответ на вопрос: {self.question.text}'
