from django_filters.rest_framework import DjangoFilterBackend
from polls.models import Poll, Question, Answer
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import viewsets, generics
from inquirer_api.permissions import IsAdminUserOrReadOnly, IsOwnerFilterBackend, ReadOnly
from rest_framework.response import Response
from django.utils import timezone


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.exclude(end_date__lte=timezone.now())
    serializer_class = PollSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poll']


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend, IsOwnerFilterBackend]
    filterset_fields = ['user', 'session_key']

    def perform_create(self, serializer):
        if not self.request.session.session_key:
            self.request.session.save()
        session_key = self.request.session.session_key
        serializer.save(user=self.request.user, session_key=session_key)


class UserAnswersView(generics.GenericAPIView):
    def get(self, request, format=None):
        if str(request.user) == 'AnonymousUser':
            data = Answer.objects.filter(session_key=request.session.session_key)
        else:
            data = Answer.objects.filter(user=request.user)
        response = {f"{item.name}. Максимум очков: {item.max_points()}": answers_for_poll(data, item.pk) for item in
                    Poll.objects.exclude(end_date__lte=timezone.now())}
        return Response(response)


def answers_for_poll(data, poll_id):
    response = []
    for result in data:
        question = {
            "Вопрос": result.question.text,
            "Тип вопроса": result.question.question_type,
            "Ответ": [choice[0] for choice in list(result.multiple_choice.values_list('title'))],
        }
        if result.question.question_type == 'single':
            question.update({"Варианты ответа": result.single_choice.title})
        if result.question.question_type == 'text':
            question.update({"Текстовый ответ": result.text})
        if poll_id == result.question.poll.id:
            question.update({"Получено очков": result.earned_points()})
            response.append(question)
    return response
