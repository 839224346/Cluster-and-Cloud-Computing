import copy,json

import json
import couchdb

new_lga_id = [20110, 20260, 20570, 20660, 20740, 20830, 20910, 21010, 21110, 21180, 21270, 21370, 21450, 21610, 21670, 21750, 21830, 21890, 22110, 22170, 22250, 22310, 22410, 22490, 22620, 22670, 22750, 22830, 22910, 22980, 23110, 23190, 23270, 23350, 23430, 23670, 23810, 23940, 24130, 24210, 24250, 24330, 24410, 24600, 24650, 24780, 24850, 24900, 24970, 25060, 25150, 25250, 25340, 25430, 25490, 25620, 25710, 25810, 25900, 25990, 26080, 26170, 26260, 26350, 26430, 26490, 26610, 26670, 26700, 26730, 26810, 26890, 26980, 27070, 27170, 27260, 27350, 27450, 27630]

def processview(view):
    new_lga_id = [20110, 20260, 20570, 20660, 20740, 20830, 20910, 21010, 21110, 21180, 21270, 21370, 21450, 21610, 21670, 21750, 21830, 21890, 22110, 22170, 22250, 22310, 22410, 22490, 22620, 22670, 22750, 22830, 22910, 22980, 23110, 23190, 23270, 23350, 23430, 23670, 23810, 23940, 24130, 24210, 24250, 24330, 24410, 24600, 24650, 24780, 24850, 24900, 24970, 25060, 25150, 25250, 25340, 25430, 25490, 25620, 25710, 25810, 25900, 25990, 26080, 26170, 26260, 26350, 26430, 26490, 26610, 26670, 26700, 26730, 26810, 26890, 26980, 27070, 27170, 27260, 27350, 27450, 27630]
    list1={}
    for row in view:
        list1[row.key]= row.value
    
    list2 = {}
    for lga in new_lga_id:
        if list1.get(lga,"NA") != "NA":
            list2[lga] =list1[lga]
        else:
            list2[lga] = 0 
            
    result = []
    for lga in new_lga_id:
        result.append(list2[lga])
    return result


couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
try:
    db = couch.create('ccc')
except:
    db = couch['ccc']

mytemp = db.get('_design/example')
if mytemp is not None:
    del db['_design/example']
    
viewData = {
"tweetnum":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){  emit(doc.rows[i].lga_code, 1)};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"emotion_1":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"positive\") { emit(doc.rows[i].lga_code, 1);}}}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"emotion_2":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"neutral\") { emit(doc.rows[i].lga_code, 1);}}}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"emotion_3":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"negative\") { emit(doc.rows[i].lga_code, 1);}}}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"emotionscore":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){  emit(doc.rows[i].lga_code, doc.rows[i].polarity_value)};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"possub":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"positive\" && doc.rows[i].subjectivity == \"subjective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"posobj":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"positive\" && doc.rows[i].subjectivity == \"objective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"neusub":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"neutral\" && doc.rows[i].subjectivity == \"subjective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"neuobj":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"neutral\" && doc.rows[i].subjectivity == \"objective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"negsub":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"negative\" && doc.rows[i].subjectivity == \"subjective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 },
"negobj":{
    "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if(doc.rows[i].polarity == \"negative\" && doc.rows[i].subjectivity == \"objective\"){emit(doc.rows[i].lga_code, 1)}};}",
    "reduce":"function (key, values) {  return sum(values); }"
 }
}
db['_design/example'] = dict(language='javascript', views=viewData)

tweetnum_view = db.view('example/tweetnum',group = True)
emotion_1_view = db.view('example/emotion_1',group = True)
emotion_2_view = db.view('example/emotion_2',group = True)
emotion_3_view = db.view('example/emotion_3',group = True)
emotionscore_view = db.view('example/emotionscore',group = True)
possub_view = db.view('example/possub',group = True)
posobj_view = db.view('example/posobj',group = True)
neusub_view = db.view('example/neusub',group = True)
neuobj_view = db.view('example/neuobj',group = True)
negsub_view = db.view('example/negsub',group = True)
negobj_view = db.view('example/negobj',group = True)


# tweetnum 
score={}
for row in tweetnum_view:
    score[row.key]= row.value

tweet_num = {}
for lga in new_lga_id:
    if score.get(lga,"NA") != "NA":
        tweet_num[lga] = score[lga]
    else:
        tweet_num[lga] = 0
tweet_num_arr = []
for lga in new_lga_id:
    tweet_num_arr.append(tweet_num[lga])
    
# positive 
positive_list={}
for row in emotion_1_view:
    positive_list[row.key]= row.value

positive_num = {}
for lga in new_lga_id:
    if positive_list.get(lga,"NA") != "NA":
        positive_num[lga] = positive_list[lga]
    else:
        positive_num[lga] = 0
        
# neutral 
neutral_list={}
for row in emotion_2_view:
    neutral_list[row.key]= row.value

neutral_num = {}
for lga in new_lga_id:
    if neutral_list.get(lga,"NA") != "NA":
        neutral_num[lga] = neutral_list[lga]
    else:
        neutral_num[lga] = 0
        
# negative 
negative_list={}
for row in emotion_3_view:
    negative_list[row.key]= row.value

negative_num = {}
for lga in new_lga_id:
    if negative_list.get(lga,"NA") != "NA":
        negative_num[lga] = negative_list[lga]
    else:
        negative_num[lga] = 0


major_emotion = []
for i in range(len(negative_num)):
    if(max(positive_num[new_lga_id[i]],neutral_num[new_lga_id[i]],negative_num[new_lga_id[i]]) == positive_num[new_lga_id[i]]):
        major_emotion.append("positive")
    elif(max(positive_num[new_lga_id[i]],neutral_num[new_lga_id[i]],negative_num[new_lga_id[i]]) == neutral_num[new_lga_id[i]]):
        major_emotion.append("neutral")
    else:
        major_emotion.append("negative")

emotion_component = []
for i in range(len(negative_num)):
    newemo = {'positive': 0, 'negative': 0, 'neutral': 0}
    newemo["positive"] = positive_num[new_lga_id[i]]
    newemo["neutral"] = positive_num[new_lga_id[i]]
    newemo["negative"] = positive_num[new_lga_id[i]]
    newemojson = copy.deepcopy(newemo)
    emotion_component.append(newemojson)

# emotion score
emotion_result={}
for row in emotionscore_view:
    emotion_result[row.key]= row.value
    
emotion_num = {}
for lga in new_lga_id:
    if emotion_result.get(lga,"NA") != "NA":
        emotion_num[lga] = round(emotion_result[lga],2)
    else:
        emotion_num[lga] = 0 
    
emotion_score = []
for lga in new_lga_id:
    emotion_score.append(emotion_num[lga])

possub_result = processview(possub_view)
posobj_result = processview(posobj_view)
neusub_result = processview(neusub_view)
neuobj_result = processview(neuobj_view)
negsub_result = processview(negsub_view)
negobj_result = processview(negobj_view)

result = {}
result["tweet_num"] = tweet_num_arr
result["major_emotion"] = major_emotion
result["emotion_component"] = emotion_component
result["emotion_score"] = emotion_score
result["possub_result"] = possub_result
result["posobj_result"] = posobj_result
result["neusub_result"] = neusub_result
result["neuobj_result"] = neuobj_result
result["negsub_result"] = negsub_result
result["negobj_result"] = negobj_result

try:
    db = couch['ccc_re']
except:
    db = couch.create('ccc_re')
mytemp2 = db.get('re')
if mytemp2 is not None:
    del db['re']    
db['re'] = result