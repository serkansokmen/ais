from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Question, SentimentResult

User = get_user_model()


class SentimentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentResult
        fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):
    query = serializers.CharField(max_length=250)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Question
        fields = ['query', 'user', 'results']
        depth = 1
