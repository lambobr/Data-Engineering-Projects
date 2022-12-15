try:
    import tweepy
    from datetime import datetime
    import pandas as pd
except Exception as e:
    print("Error : {} ".format(e))


consumer_key = 'kFNZqoQBOEEFmSqbWZBY25h2r'
consumer_secret = 'xWEoAhQu5EY52XLgjShiJyDO2W3irD2xiteVbF4lMkPfT7Zksv'
access_token = '927776582088847361-VZ3Xx2fxA7TUNkqMBvGcVm6XiY2SXoz'
access_token_secret = 'nguoreIyRw0oQIkBpILRcrbpFxCSxweYwVlyV1tTqJv9a'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEQtjgEAAAAAIzWl9i62pWrcpo24EcVRWk1UfNA%3DimnVyFwJFOEYPA3RQ9phXXC9rBgSuXokkLWwcZwGNxzhZi7v3e'

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

class TweetsExtract:
    def __init__(self, twitter_id: int, tweet_count: int):
        self.twitter_id = twitter_id
        self.tweet_count = tweet_count
        self.tweet_list = []
        self.auth()

    def auth(self):
        self.object = client.get_users_tweets(id=self.twitter_id,
                                         max_results=self.tweet_count,
                                         user_auth=True,
                                         tweet_fields=['created_at', 'text']
                                         )

    def tweets(self):
        for content in self.object.data:
            tweet_text = content['text'].lower()
            tweet_date = datetime.strftime(content['created_at'],"%Y-%m-%d %H:%M:%S")
            self.tweet_list.append([tweet_date, tweet_text])

        tweet_df = pd.DataFrame(self.tweet_list, columns=["tweet_datetime","tweet"], dtype="string")
        return tweet_df



