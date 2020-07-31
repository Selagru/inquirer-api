from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=255, help_text='Название опроса')
    start_date = models.DateTimeField(auto_now_add=True, editable=False, help_text='Дата старта')
    end_date = models.DateTimeField(null=True, blank=True, help_text='Дата окончания')
    description = models.TextField(help_text='Описание опроса')

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):

    QUESTION_TYPE = (
        ('text', 'ответ текстом'),
        ('o_ch', 'ответ с выбором одного варианта'),
        ('m_ch', 'ответ с выбором нескольких вариантов'),
    )

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    text = models.CharField(max_length=4096, help_text='Текст вопроса')
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPE,
                                     default='text', help_text='Тип вопроса')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.text} type: {self.question_type}'


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    title = models.CharField(max_length=4096, help_text='Текст выбора')

    def lock_other(self):
        if self.question.question_type == 'o_ch':
            return True
        return False

    def __str__(self):
        return self.title


class Answer(models.Model):
    session_id = models.CharField(max_length=32)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ManyToManyField('Choice', blank=True)
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_text(self):
        if self.question.question_type == 'text':
            return True
        return False

    def is_one_choice(self):
        if self.question.question_type == 'o_ch':
            return True
        return False

    def is_multiple_choices(self):
        if self.question.question_type == 'm_ch':
            return True
        return False

    def __str__(self):
        return f'Ответ на вопрос: {self.question.text}'
