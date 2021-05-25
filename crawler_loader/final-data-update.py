from datetime import datetime
import json
import couchdb

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('final')
except:
    db = couch['final']
    
with open('final.txt', 'r') as f:
    count = 0
    tweet_list =[]
    for line in f:
        count += 1
        tweet = json.loads(line)

        db.save(tweet)
