from rest_framework import viewsets, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .analyser import search_textblob, search_vader
from .serializers import UserSerializer, QuestionSerializer


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
        serializer = QuestionSerializer(data=request.data)
        use_vader = request.query_params.get('use_vader')
        if serializer.is_valid():
            query = serializer.validated_data['query']
            serializer.validated_data['user'] = request.user
            serializer.save(user=request.user)

            if use_vader is not None:
                results = search_vader(query)
                return Response({"results": results},
                                status=status.HTTP_200_OK)
            else:
                results = search_textblob(query)
                return Response({"results": results},
                                status=status.HTTP_200_OK)
        return Response("Query required",
                        status=status.HTTP_400_BAD_REQUEST)
