from datetime import datetime
import json
import couchdb
import os

couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('ccc')
except:
    db = couch['ccc']
    
txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
if len(txt_files) != 1:
    raise ValueError('should be only one txt file in the current directory')

filename = txt_files[0]
with open(filename, 'r') as f:
    count = 0
    for line in f:
        count += 1
        tweet = json.loads(line)[0]
        #if count % 100000 == 0: 
            #print(count//100000)
        
        timestamp = int(datetime.strptime(tweet['created_at'], "%Y-%m-%d %H:%M:%S").timestamp())
        tweet['created_at']  = timestamp
        tweet['_id'] = str(tweet['tweet_id'])
        db.save(tweet)
        if count ==500000: break