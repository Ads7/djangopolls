from .models import Question
from rest_framework import serializers
from django.contrib.auth.models import User
import logging
from google.appengine.api import search

index = search.Index(name='question')

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
        key=question.put()
        fields = [
            search.TextField(name="id", value=key.urlsafe()), # the product id
            search.TextField(name="question_text", value=validated_data["question_text"])
        ]
        d = search.Document(doc_id=key.urlsafe(),fields=fields)
        try:
            val=index.put(d)
            logger.error("index"+val[0].id)
        except search.Error:
            logger("indexing failed")

        return question




