import tweepy
from shapely.geometry import shape, point
import json
import pickle
import random
from textblob import TextBlob
import couchdb
import yake
from datetime import datetime
import time
import traceback
import os

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('ccc')
except:
    db = couch['ccc']

# load map
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'vic_map.p')

melb_map = pickle.load(open(filename,'rb'))
for k,v in melb_map.items():
    melb_map[k] = shape(v)

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="YXw9gwB4e9ZwoR3iK1CNOpL3O"
consumer_secret="TpiEMr3yFikEQcOYhSypYydFoXkhAvNXTUuTekn0AopsC3zU0I"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1384454457241399296-YsKp0rEj6fkDI0sOz4Lt4Xm1vr7dxi"
access_token_secret="WSb6oMpBznjwdDoJLwkdMc7wMBWF6VcIn3wdkNNhU7ESi"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

def extract_tweet_attributes(tweet_object, suburb):
    # create empty list
    tweet_list =[]
    # loop through tweet objects
    for tweet in tweet_object:
        tweet_id = tweet.id # unique integer identifier for tweet
        text = tweet.text # utf-8 text of tweet
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        created_at = str(tweet.created_at) # utc time tweet created
        # append attributes to list
        tweet_list.append({
            'tweet_id':tweet_id, 
            'text':text, 
            'favorite_count':favorite_count,
            'retweet_count':retweet_count,
            'created_at':created_at,
            'lga_code':suburb})

    return tweet_list


def extract_keyword(text):
    kw_extractor = yake.KeywordExtractor()
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.2
    numOfKeywords = 4
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    
    return [kw[0].lower() for kw in keywords]


tweet_list = []
while True:
    suburb, shape = random.choice(list(melb_map.items()))
    coords = shape.centroid.coords[0]
    search = "covid"
    geocode = str(coords[1]) + ',' + str(coords[0]) + ',5km'
    tweets = None
    try:
        tweets = tweepy.Cursor(
            api.search,
            q=search,
            lang="en",
            geocode=geocode,
            result_type='recent',
            until=datetime.now().strftime("%Y-%m-%d"),
            count=100).items(100)
        tweets = extract_tweet_attributes(tweets, suburb)
        search_limit = api.rate_limit_status()['resources']['search']['/search/tweets']
#         print(search_limit)
#         print('reset:', datetime.fromtimestamp(search_limit['reset']).strftime("%Y-%m-%d %H:%M:%S"))
#         print(len(tweets))
        for tweet in tweets:
            polarity, subjectivity = TextBlob(tweet['text']).sentiment
            p, s = '' ,''
            if polarity < -0.05:
                p = 'negative'
            elif polarity < 0.05:
                p = 'neutral'
            else:
                p = 'positive'

            if subjectivity < 0.5:
                s = 'objective'
            else:
                s = 'subjective'

            tweet['polarity_value'] = polarity
            tweet['polarity'] = p
            tweet['subjectivity'] = s
            tweet['keywords'] = extract_keyword(tweet['text'])
        tweet_list.extend(tweets)
    except Exception:
        # traceback.print_exc()
        break
# print('new tweets: ', len(tweet_list))

for tweet in tweet_list:
    timestamp = int(datetime.strptime(tweet['created_at'], "%Y-%m-%d %H:%M:%S").timestamp())
    tweet['created_at']  = timestamp
    tweet['_id'] = str(tweet['tweet_id'])

# save data
try:
    db.update(tweet_list)
except:
    print('Update error!')