from django.urls import path
import ais.core.views as views


urlpatterns = [
    path('', views.HelloView.as_view(), name='hello'),
    path('sentiment/', views.SentimentView.as_view(), name='sentiment'),
]
