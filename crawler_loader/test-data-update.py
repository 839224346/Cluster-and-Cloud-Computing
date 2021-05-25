from datetime import datetime
import json
import couchdb

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('realtime')
except:
    db = couch['realtime']
    

# if len(txt_files) != 1:
#     raise ValueError('should be only one txt file in the current directory')


filename = 'sample-1000.txt'
with open(filename, 'r') as f:
    count = 0
    tweet_list =[]
    for line in f:
        count += 1
        tweet = json.loads(line)
        timestamp = int(datetime.strptime(tweet['created_at'], "%Y-%m-%d %H:%M:%S").timestamp())
        tweet['created_at']  = timestamp
        tweet['_id'] = str(tweet['tweet_id'])
        db.save(tweet)
