from rest_framework import serializers
from polls.models import Poll, Question, SingleChoice, MultipleChoice, Answer


class SingleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChoice
        fields = ['pk', 'title', 'points', 'lock_other', 'is_correct']


class MultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoice
        fields = ['pk', 'title', 'points', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    singlechoice_set = MultipleChoiceSerializer(many=True, required=False)
    multiplechoice_set = MultipleChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['pk', 'text', 'question_type', 'singlechoice_set', 'multiplechoice_set']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Poll
        fields = ['pk', 'name', 'description', 'end_date', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('question_set')


        poll = Poll.objects.create(**validated_data)
        for question in questions_data:
            single_choice_data = question.pop('singlechoice_set', None)
            multiple_choice_data = question.pop('multiplechoice_set', None)
            inst = Question.objects.create(poll=poll, **question)
            if single_choice_data:
                for single_choice in single_choice_data:
                    SingleChoice.objects.create(question=inst, **single_choice)
            if multiple_choice_data:
                for multiple_choice in multiple_choice_data:
                    MultipleChoice.objects.create(question=inst, **multiple_choice)
        return poll


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', required=False)
    session_key = serializers.ReadOnlyField()

    class Meta:
        model = Answer
        fields = ['user', 'session_key', 'text', 'question', 'single_choice', 'multiple_choice', 'earned_points']

    def create(self, validated_data):
        if str(validated_data['user']) == 'AnonymousUser':
            validated_data.pop('user')
            old_answers = Answer.objects.filter(session_key=validated_data['session_key'],
                                                question=validated_data['question'])
            if old_answers.first() is not None:
                raise serializers.ValidationError("Вы уже отвечали на данный вопрос.")
        else:
            old_answers = Answer.objects.filter(user=validated_data['user'], question=validated_data['question'])
            if old_answers.first() is not None:
                raise serializers.ValidationError(
                    f"Пользователь {validated_data['user']} уже отвечал на данный вопрос.")

        text = validated_data.pop('text')
        single_choice = validated_data.pop('single_choice')
        multiple_choice = validated_data.pop('multiple_choice')
        answer = Answer.objects.create(**validated_data)

        if answer.is_text():
            answer.text = text
            answer.save()
            return answer

        if answer.is_one_choice():
            if single_choice in answer.question.singlechoice_set.all():
                answer.single_choice = single_choice
                answer.save()
                return answer
            else:
                answer.delete()
                raise serializers.ValidationError("The answer does not belong to this question"
                                                  " or you didn't make a choice")
        elif single_choice:
            question_type = answer.question.question_type
            answer.delete()
            raise serializers.ValidationError(f"You pick SINGLE choice answer for question type: {question_type}")

        if answer.is_multiple_choices():
            for choice in multiple_choice:
                if choice in answer.question.multiplechoice_set.all():
                    answer.multiple_choice.add(choice)
                else:
                    answer.delete()
                    raise serializers.ValidationError("The answer does not belong to this question.")
            answer.save()
            return answer
        elif multiple_choice:
            question_type = answer.question.question_type
            answer.delete()
            raise serializers.ValidationError(f"You pick MULTIPLE choice answer for question type: {question_type}")

        return serializers.ValidationError("Unknown question type.")
