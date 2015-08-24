from .models import Choice,Question
from rest_framework import serializers
from django.contrib.auth.models import User
import logging
from google.appengine.ext import ndb
from google.appengine.api import search

index = search.Index(name='question')
logger = logging.getLogger(__name__)

class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField()
    votes = serializers.IntegerField(default=0,allow_null=True)


class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField()
    choices = serializers.ListField(child=ChoiceSerializer(),allow_null=True)
    image=serializers.CharField(default=None,allow_null=True)

    def create(self, validated_data):
        question = Question()
        logger.info(validated_data)
        question.question_text=validated_data["question_text"]
        choice_list=[]
        for choice in validated_data["choices"]:
            choice_list.append(Choice(choice_text=str(choice["choice_text"])))
        question.choices=choice_list
        key=question.put()
        fields = [
            search.TextField(name="id", value=str(key.id())), # the product id
            search.TextField(name="question_text", value=validated_data["question_text"])
        ]
        d = search.Document(doc_id=str(key.id()),fields=fields)
        try:
            val=index.put(d)
        except search.Error:
            logger("indexing failed")

        return question
