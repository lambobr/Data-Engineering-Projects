from extract import TweetsExtract
import re

# twitter id and count of tweets to extract:
ID = 44196397
COUNT = 100

data = TweetsExtract(twitter_id = ID,tweet_count = COUNT)
tweets = data.tweets()

def enrich_data(tweets):
    # if tweet contains crypto related stuff, then flag as 1 else 0
    for index,row in tweets.iterrows():
        if re.match('.*(bitcoin|btc|doge|crypto|dogecoin).*',row['tweet']):
            tweets.loc[index,'crypto'] = str(1)
        else:
            tweets.loc[index,'crypto'] = str(0)

    tweets['tweet_date']= tweets['tweet_datetime'].str.split(expand=True)[0]
    tweets['tweet_time'] = tweets['tweet_datetime'].str.split(expand=True)[1]
    tweets['tweet_hour'] = tweets['tweet_time'].str.split(pat=":", expand=True)[0]

    return tweets

def convert_to_json(enriched_tweets):
    #convert to json since data contains comma so converting to_csv messes up the whole file

    tweets_json = enriched_tweets.to_json(orient='records',lines=True)
        #orient and lines are needed options to make a newline delimited json file

    return tweets_json

enriched_tweets = enrich_data(tweets)
tweets_json = convert_to_json(enriched_tweets)


