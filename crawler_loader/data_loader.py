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
        

