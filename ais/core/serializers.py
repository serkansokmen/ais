from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['query']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'usermame']
        depth = 1
