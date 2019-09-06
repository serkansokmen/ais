import tweepy
import textblob
from django.conf import settings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                           settings.TWITTER_CONSUMER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,
                      settings.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def search_textblob(query):
    tweets = api.search(query)

    def analyze(tweet):
        polarity = textblob.TextBlob(tweet.text).sentiment.polarity
        subjectivity = textblob.TextBlob(tweet.text).sentiment.subjectivity
        return {
            'tweet': tweet.text,
            'polarity': polarity,
            'subjectivity': subjectivity,
        }

    return map(analyze, tweets)


def search_vader(query):
    tweets = api.search(query)

    def analyze(tweet):
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(tweet.text)
        return {
            'tweet': tweet.text,
            'score': score,
        }
    return map(analyze, tweets)
