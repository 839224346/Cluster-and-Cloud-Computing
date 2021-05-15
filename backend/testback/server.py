import couchdb
import requests
import flask,json
from flask import request
from collections import Counter

server = flask.Flask(__name__)


@server.route('/api/statistics/zone/melbourn',methods=['get'])
def statistics():  
    
    get_data = request.args.to_dict()
    begintime = get_data.get('begintime')
    endtime = get_data.get('endtime')

    starttime = begintime
    endtime = endtime

    file1=open('api_1.json')
    api1=json.load(file1)

    new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
    new_lga_name = ['Banyule', 'Bayside','Boroondara','Brimbank','Cardinia','Casey','Darebin','Frankston','Glen Eira','Greater Dandenong','Hobsons Bay','Hume','Knox','Macedon Ranges','Manningham','Maribyrnong','Maroondah','Melbourne','Melton','Mitchell','Monash','Moonee Valley','Moorabool','Moreland','Mornington Peninsula','Murrindindi','Nillumbik','Port Phillip','Stonnington','Whitehorse','Whittlesea','Wyndham','Yarra','Yarra Ranges']

    couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
    db = couch['ccc']
    
    mytemp = db.get('_design/example')
    if mytemp is not None:
        del db['_design/example']

    viewData = {
    "score":{
        "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if ( new Date(doc.rows[i].created_at).getTime() > "+ starttime +  " && new Date(doc.rows[i].created_at).getTime() <"+ endtime +") emit(doc.rows[i].lga_code, 1)};}",
        "reduce":"function (key, values) {  return sum(values); }"
        },
    "emotion":{
        "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if ( new Date(doc.rows[i].created_at).getTime() > "+ starttime +  " && new Date(doc.rows[i].created_at).getTime() <"+ endtime +") emit(doc.rows[i].lga_code, doc.rows[i].emotion)};}",
        "reduce":"function (key, values) {  return values; }"
        },
    "keyword":{
        "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if ( new Date(doc.rows[i].created_at).getTime() > "+ starttime +  " && new Date(doc.rows[i].created_at).getTime() <"+ endtime +") emit(doc.rows[i].lga_code, doc.rows[i].keywords)};}",
        "reduce":"function (key, values) {  return values; }"
        }
    }
    db['_design/example'] = dict(language='javascript', views=viewData)

    score_view = db.view('example/score',group = True)
    emotion_view = db.view('example/emotion',group = True)
    keyword_view = db.view('example/keyword',group = True)


    # score 
    score={}
    for row in score_view:
        score[row.key]= row.value

    covid_attention = {}
    for lga in new_lga_id:
        if score.get(lga,"NA") != "NA":
            covid_attention[lga] = score[lga]
        else:
            covid_attention[lga] = 0 


    # emotion 
    emotion_result={}
    for row in emotion_view:
        emotion_result[row.key]= row.value

    
    major_emotion = {}
    emotion_component = {}
    for lga in new_lga_id:
        if emotion_result.get(lga,"NA") != "NA":
            emotion_data = emotion_result[lga][0]
            emotion_counter = Counter(emotion_data)
            majority = emotion_counter.most_common(1)[0][0]
            major_emotion[lga] = majority
            emotion_component[lga] = dict(emotion_counter)
        else:
            major_emotion[lga] = ""
            emotion_component[lga] = {}    
    

    # keyword
    keyword={}
    for row in keyword_view:
        keyword[row.key]= row.value

    keyword_data = {}
    for lga in new_lga_id:
        key_list = []
        if keyword.get(lga,"NA") != "NA":        
            for each in keyword[lga][0]:
                key_list.extend(each)
            keydict = dict(Counter(key_list))  
            keyword_list = []
            for k in keydict:
                text={}
                text["text"] = k
                text["value"] = keydict[k]
                keyword_list.append(text)      
            keyword_data[lga] = keyword_list
        else:
            keyword_data[lga] = []

    for i in range(len(api1["features"])):
        api1["features"][i]["properties"]["covid_attention"] = covid_attention[api1["features"][i]["properties"]["lga_id"]]
        api1["features"][i]["properties"]["major_emotion"] = major_emotion[api1["features"][i]["properties"]["lga_id"]]
        api1["features"][i]["properties"]["emotion_component"] = emotion_component[api1["features"][i]["properties"]["lga_id"]]
        api1["features"][i]["properties"]["key_words"] = keyword_data[api1["features"][i]["properties"]["lga_id"]]

    return json.dumps(api1, ensure_ascii=False)




@server.route('/api/statistics/relationship',methods = ['post'])
def queryRelationship():

    da=json.loads(request.data)


    begintime = da.get('begintime')
    endtime = da.get('endtime')
    query_lga = da.get('lga_id')
    # query_lga = request.form.getlist("lga_id")

    starttime = begintime
    endtime = endtime

    # query_lga=[20660,22170]

    file2=open('api_2.json')
    api2=json.load(file2)

    new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]

    couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
    db = couch['ccc']

    mytemp = db.get('_design/example2')
    if mytemp is not None:
        del db['_design/example2']
    
    viewData = {
    "tweetnum":{
        "map":"function(doc){ for (i = 0; i < doc.rows.length; i++){ if ( new Date(doc.rows[i].created_at).getTime() > "+ starttime +  " && new Date(doc.rows[i].created_at).getTime() <"+ endtime +") emit(doc.rows[i].lga_code, 1)};}",
        "reduce":"function (key, values) {  return sum(values); }"
        }
    }
    db['_design/example2'] = dict(language='javascript', views=viewData)

    tweetnum_view = db.view('example2/tweetnum',group = True)
    
    tnum_result={}
    for row in tweetnum_view:
        tnum_result[row.key]= row.value
    
    tweet_num = {}
    for lga in new_lga_id:
        if tnum_result.get(lga,"NA") != "NA":
            tweet_num[lga] = tnum_result[lga]
        else:
            tweet_num[lga] = 0 

    api2_tnum = []
    for lga in new_lga_id:
        api2_tnum.append(tweet_num[lga])

    lgaid_i_map = {"20660": 0, "20910": 1, "21110": 2, "21180": 3, "21450": 4, "21610": 5, "21890": 6, "22170": 7, "22310": 8, "22670": 9, "23110": 10, "23270": 11, "23670": 12, "24130": 13, "24210": 14, "24330": 15, "24410": 16, "24600": 17, "24650": 18, "24850": 19, "24970": 20, "25060": 21, "25150": 22, "25250": 23, "25340": 24, "25620": 25, "25710": 26, "25900": 27, "26350": 28, "26980": 29, "27070": 30, "27260": 31, "27350": 32, "27450": 33}
 

    fin_lga_name = []
    fin_emotion_score = []
    fin_tweet_num = []
    fin_GP_num = []
    fin_education_rank = []
    fin_population_num = []
    fin_averge_income = []
    fin_averge_age = []
    fin_homeless_rate = []

    for each in query_lga:
        index = lgaid_i_map[str(each)]
    
        fin_lga_name.append(api2["data"]["lga_name"][index])
        fin_emotion_score.append(0)
        fin_tweet_num.append(api2_tnum[index])
        fin_GP_num.append(api2["data"]["factor"]["GP_num"][index])
        fin_education_rank.append(api2["data"]["factor"]["education_rank"][index])
        fin_population_num.append(api2["data"]["factor"]["population_num"][index])
        fin_averge_income.append(api2["data"]["factor"]["averge_income"][index])
        fin_averge_age.append(api2["data"]["factor"]["averge_age"][index])
        fin_homeless_rate.append(api2["data"]["factor"]["homeless_rate"][index])
    
    api2["data"]["lga_name"] = fin_lga_name
    api2["data"]["factor"]["tweet_num"] = fin_tweet_num
    api2["data"]["factor"]["emotion_score"] = fin_emotion_score
    api2["data"]["factor"]["GP_num"] = fin_GP_num
    api2["data"]["factor"]["education_rank"] = fin_education_rank
    api2["data"]["factor"]["population_num"] = fin_population_num
    api2["data"]["factor"]["averge_income"] = fin_averge_income
    api2["data"]["factor"]["averge_age"] = fin_averge_age
    api2["data"]["factor"]["homeless_rate"] = fin_homeless_rate

    return json.dumps(api2, ensure_ascii=False)



server.run(port = 3000,debug = True,host = '0.0.0.0',threaded = True)
