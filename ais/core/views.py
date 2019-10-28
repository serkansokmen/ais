from rest_framework import viewsets, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AnalyticsSerializer, SentimentResultSerializer
from .models import Question, SentimentResult
from .analyser import search

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib


class HelloView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, world!'}
        return Response(content)


class SentimentView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        query = request.data.get('query', None)
        results = []

        if query is not None:
            instance, created = Question.objects.get_or_create(query=query,
                                                               user=request.user,)
            results = search(query)
            for obj in instance.results.all():
                obj.delete()
            for result in results:
                # tweet_data = result['tweet']
                SentimentResult.objects.create(text=result['text'],
                                               compound=result['compound'],
                                               positive=result['positive'],
                                               negative=result['negative'],
                                               neutral=result['neutral'],
                                               polarity=result['polarity'],
                                               subjectivity=result['subjectivity'],
                                               question=instance,)
            serializer = AnalyticsSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Data not in correct format",
                        status=status.HTTP_400_BAD_REQUEST)


class VerifyCreditCardTransaction(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        vector = pd.DataFrame([request.json])
        loaded_model = joblib.load(filename)
        res = str(loaded_model.predict(vector)[0])
        result = {
            'id': 0,
            'prediction': res
        }
        return Response(result, status=status.HTTP_200_OK)
