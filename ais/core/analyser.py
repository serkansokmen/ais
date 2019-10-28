import tweepy
import textblob
from django.conf import settings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                           settings.TWITTER_CONSUMER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                      settings.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def analyze(tweet):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(tweet.text)
    sentiment = textblob.TextBlob(tweet.text).sentiment
    return {
        'text': tweet.text,
        'compound': score['compound'],
        'positive': score['pos'],
        'negative': score['neg'],
        'neutral': score['neu'],
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity,
    }


def search(query):
    tweets = api.search(query)

    return list(map(analyze, tweets))
