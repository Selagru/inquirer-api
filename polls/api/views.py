from django_filters.rest_framework import DjangoFilterBackend
from polls.models import Poll, Question, Answer, Choice
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer
from rest_framework.response import Response
from rest_framework import generics, viewsets
from inquirer_api.permissions import IsAdminUserOrReadOnly
from django.utils import timezone
from rest_framework import permissions


def answers_for_poll(data, poll_id):
    response = []
    for result in data:
        question = {
            "Вопрос": result.question.text,
            "Тип вопроса": result.question.question_type,
            "Текстовый ответ": result.text,
            "Варианты ответа": [choice[0] for choice in list(result.choice.values_list('title'))]
        }
        if poll_id == result.question.poll.id:
            response.append(question)
    return response


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.exclude(end_date__lte=timezone.now())
    serializer_class = PollSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poll']


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question', 'question__poll']


class AnswerView(generics.GenericAPIView):
    serializer_class = AnswerSerializer

    def post(self, request, format=None):
        answer = AnswerSerializer(data=request.data, context=request)
        if answer.is_valid(raise_exception=True):
            answer.save()
            return Response({'result': 'OK. Ваши ответы приняты'})

    def get(self, request, format=None):
        data = Answer.objects.filter(session_id=request.session.session_key)
        response = {item.name: answers_for_poll(data, item.pk) for item in Poll.objects.exclude(end_date__lte=timezone.now())}
        return Response(response)
