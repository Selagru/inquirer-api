from rest_framework import serializers
from polls.models import Poll, Question, Choice, Answer


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['pk', 'title', 'lock_other']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')

    class Meta:
        model = Question
        fields = ['pk', 'text', 'question_type', 'choices']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Poll
        fields = ['pk', 'name', 'description', 'end_date', 'questions']


class AnswerSerializer(serializers.Serializer):
    answers = serializers.JSONField()

    def validate_answers(self, answers):
        if not answers:
            raise serializers.ValidationError("Answers must be not null.")
        return answers

    def save(self):
        if not self.context.session.session_key:
            self.context.session.save()
        session_id = self.context.session.session_key
        # user = self.context.user

        row_answers = self.data['answers']
        for question_id in row_answers.keys():
            question = Question.objects.get(pk=question_id)
            for answers in row_answers[question_id].values():
                if question.question_type == 'o_ch':
                    choice = Choice.objects.get(pk=answers)
                    answer = Answer.objects.create(session_id=session_id, question=question)
                    answer.choice.add(choice)
                elif question.question_type == 'm_ch':
                    choice = Choice.objects.filter(pk__in=answers)
                    answer = Answer.objects.create(session_id=session_id, question=question)
                    for x in choice:
                        answer.choice.add(x)
                elif question.question_type == 'text':
                    Answer.objects.create(session_id=session_id, question=question, text=answers)
