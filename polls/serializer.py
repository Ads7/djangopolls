from .models import Choice ,Question
from rest_framework import serializers
from django.contrib.auth.models import User

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('question', 'choice_text', 'votes')
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date',"image")

# class PhotoSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Question
#         fields = ('url', 'id', 'image')
#         owner = serializers.Field(source='owner.username')
# class UserSerializer(serializers.ModelSerializer):
#     question = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'question')
