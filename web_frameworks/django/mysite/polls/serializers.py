
from .models import Question, Choice
from rest_framework import serializers


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.HyperlinkedRelatedField(
        many=True, view_name='polls:detail',
        read_only=True, lookup_field='username')

    class Meta:
        model = Choice
        fields = ('question', 'choice_text', 'votes')
