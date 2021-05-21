from datetime import datetime
import json
import couchdb

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('ccc')
except:
    db = couch['ccc']
    
with open('processed-9M.txt', 'r') as f:
    count = 0
    tweet_list = []
    for line in f:
        count += 1
        tweet_list += json.loads(line),
        if count % 10000 == 0: 
            data = {}
            data['rows'] = tweet_list
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
            db[timestamp] = data
            tweet_list = []