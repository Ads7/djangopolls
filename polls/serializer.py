from .models import Question
from rest_framework import serializers
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
# class ChoiceSerializer(serializers.Serializer):
#     question_text = serializers.CharField()
#     image = serializers.CharField()
#     pub_date = serializers.DateTimeField()
#     class Meta:
#         model = Choice
#         fields = ('question', 'choice_text', 'votes')
#
class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField()

    def create(self, validated_data):
        question = Question()
        question.question_text=validated_data["question_text"]
        question.put()
        return question




