from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import twitter_credentials
import numpy as np
import pandas as pd


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    """
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    """


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,  twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,  twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        listener = TwitterListener(fetched_tweet_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords
        stream.filter(track=hash_tag_list)


# Class to print the tweets
class TwitterListener(StreamListener):
    """
    Basic listener class that prints received tweets to stdout
    """
    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on data method in case rate limit occurs
            return False
        print(status)


class TweetAnalyser():
    """
    Functionality for analysing and categorising content from Tweets
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="JoeBiden", count=10)

    df = tweet_analyser.tweets_to_data_frame(tweets)

    print(df.head(5))
    #print(tweets)
