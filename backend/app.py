import couchdb
import copy
import flask,json
from flask import request
from collections import Counter
from flask_cors import CORS
import conf
import helper


server = flask.Flask(__name__)
CORS(server, resources=r'/*')
# CORS(server, supports_credentials=True)
@server.route('/test')
def hello_world():
    return 'hello world'


@server.route('/api/statistics/zone/melbourn',methods=['get'])
def statistics():  
    
    get_data = request.args.to_dict()
    begintime = get_data.get('begintime')
    endtime = get_data.get('endtime')

    starttime = begintime
    endtime = endtime

    file1=open('api_1.json')
    api1=json.load(file1)

    lgaid_i_map = conf.lgaid_i_map
    
    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['realtime']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:
        new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
    
        mytemp = db.get('_design/example4')
        if mytemp is not None:
            del db['_design/example4']
    
        viewData = {
        "emotion_1":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"positive\" ) emit(doc.lga_code, 1);}",
            "reduce":"function (key, values) {  return sum(values); }"
        },
        "emotion_2":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"neutral\" ) emit(doc.lga_code, 1);}",
            "reduce":"function (key, values) {  return sum(values); }"
        },
        "emotion_3":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"negative\" ) emit(doc.lga_code, 1);}",
            "reduce":"function (key, values) {  return sum(values); }"
        },
        "score":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +") emit(doc.lga_code, 1);}",
            "reduce":"function (key, values) { return sum(values);}"
        },
        "keyword":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +") emit(doc.lga_code, doc.keywords);}",
            "reduce":"function (key, values) {  return values; }"
        }
        }
        db['_design/example4'] = dict(language='javascript', views=viewData)

        emotion_1_view = db.view('example4/emotion_1',group = True)
        emotion_2_view = db.view('example4/emotion_2',group = True)
        emotion_3_view = db.view('example4/emotion_3',group = True)
        score_view = db.view('example4/score',group = True)
        keyword_view = db.view('example4/keyword',group = True)


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


        # keyword
        keyword={}
        for row in keyword_view:
            keyword[row.key]= row.value

        keyword_data = {}
        for lga in new_lga_id:
            key_list = []
            if keyword.get(lga,"NA") != "NA":
                for dic in keyword[lga]:
                    for each in dic:
                        for key in each:
                            if isinstance(key, str):
                                key_list.append(key)


                keydict = dict(Counter(key_list))  
                keyword_list = []
                for k in keydict:
                    text={}
                    text[k] = keydict[k]

                    keyword_list.append(text)      
                keyword_data[lga] = keyword_list
            else:
                keyword_data[lga] = []
    
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
  
            value = positive_num[new_lga_id[i]] + neutral_num[new_lga_id[i]] + negative_num[new_lga_id[i]]
            if value != 0:
                if(max(positive_num[new_lga_id[i]],neutral_num[new_lga_id[i]],negative_num[new_lga_id[i]]) == positive_num[new_lga_id[i]]):
                    major_emotion.append("positive")
                elif(max(positive_num[new_lga_id[i]],neutral_num[new_lga_id[i]],negative_num[new_lga_id[i]]) == neutral_num[new_lga_id[i]]):
                    major_emotion.append("neutral")
                else:
                    major_emotion.append("negative")
            else:
                major_emotion.append("")


        emotion_component = []
        for i in range(len(negative_num)):
            newemo = {'positive': 0, 'negative': 0, 'neutral': 0}
            newemo["positive"] = positive_num[new_lga_id[i]]
            newemo["neutral"] = positive_num[new_lga_id[i]]
            newemo["negative"] = positive_num[new_lga_id[i]]
            newemojson = copy.deepcopy(newemo)
            emotion_component.append(newemojson)

        #final 
        final_result = helper.get_scores_from_cached_data(starttime, endtime)

# + final_result[str(api1["features"][i]["properties"]["lga_id"])]['tweet_num']
        for i in range(len(api1["features"])):
            
            for key,value in final_result[str(new_lga_id[i])]['emotion_component'].items():
                if key in emotion_component[lgaid_i_map[str(api1["features"][0]["properties"]["lga_id"])]]:
                    emotion_component[lgaid_i_map[str(api1["features"][0]["properties"]["lga_id"])]][key] += value
                else:
                    emotion_component[lgaid_i_map[str(api1["features"][0]["properties"]["lga_id"])]][key] = value
            
            emo_com_co = copy.deepcopy(emotion_component[lgaid_i_map[str(api1["features"][0]["properties"]["lga_id"])]])

            one_major_emo = ""
            value = emo_com_co['positive'] + emo_com_co['neutral'] + emo_com_co['negative']
            if value != 0:
                if(max(emo_com_co['positive'],emo_com_co['neutral'],emo_com_co['negative']) == emo_com_co['positive']):
                    one_major_emo = "positive"
                elif(max(positive_num[new_lga_id[i]],neutral_num[new_lga_id[i]],negative_num[new_lga_id[i]]) == neutral_num[new_lga_id[i]]):
                    one_major_emo = "neutral"
                else:
                    one_major_emo = "negative"
            else:
                one_major_emo = ""

            api1["features"][i]["properties"]["covid_attention"] = covid_attention[api1["features"][i]["properties"]["lga_id"]] + final_result[str(new_lga_id[i])]['tweet_num']
            api1["features"][i]["properties"]["major_emotion"] = one_major_emo
            api1["features"][i]["properties"]["emotion_component"] = emotion_component[lgaid_i_map[str(api1["features"][0]["properties"]["lga_id"])]]
            # api1["features"][i]["properties"]["key_words"] = keyword_data[api1["features"][i]["properties"]["lga_id"]]
            api1["features"][i]["properties"]["key_words"] = final_result[str(new_lga_id[i])]['keyword']

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

    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['realtime']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:
        mytemp = db.get('_design/example5')
        if mytemp is not None:
            del db['_design/example5']
    
        viewData = {
        "score":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +") emit(doc.lga_code, 1);}",
            "reduce":"function (key, values) { return sum(values);}"
        },
        "emotionscore":{
            "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +") emit(doc.lga_code, doc.polarity_value);}",
            "reduce":"function (key, values) {  return sum(values); }"
        }
        }
        db['_design/example5'] = dict(language='javascript', views=viewData)


        new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]


        score_view = db.view('example5/score',group = True)
        emotion_score_view = db.view('example5/emotionscore',group = True)

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

        # emotion score
        emotion_result={}
        for row in emotion_score_view:
            emotion_result[row.key]= row.value

        emotion_num = {}
        for lga in new_lga_id:
            if emotion_result.get(lga,"NA") != "NA":
                if covid_attention[lga] != 0:
                    emotion_num[lga] = round(emotion_result[lga] / covid_attention[lga],2)
                else:
                    emotion_num[lga] = 0
            else:
                emotion_num[lga] = 0 

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

        # final
        final_result = helper.get_scores_from_cached_data(starttime, endtime)

        for each in query_lga:
            index = lgaid_i_map[str(each)]
    
            fin_lga_name.append(api2["data"]["lga_name"][index])
            try:
                fin_emotion_score.append(emotion_num[each] + final_result[str(each)]['emotion_score'])
                fin_tweet_num.append(covid_attention[each] + final_result[str(each)]['tweet_num'])
            except Exception as error:
                
                fin_emotion_score.append(final_result[str(each)]['emotion_score'])
                fin_tweet_num.append(final_result[str(each)]['tweet_num'])

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

@server.route('/api/statistics/lgaEmotion',methods = ['post'])
def querylgaEmotion():

    da=json.loads(request.data)

    begintime = da.get('begintime')
    endtime = da.get('endtime')
    query_lga = da.get('lga_id')
    # query_lga = request.form.getlist("lga_id")

    starttime = begintime
    endtime = endtime

    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['realtime']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:

        mytemp = db.get('_design/example3')
        if mytemp is not None:
          del db['_design/example3']
    
        viewData = {
            "possub":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"positive\" && doc.subjectivity == \"subjective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            },
            "posobj":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"positive\" && doc.subjectivity == \"objective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            },
            "neusub":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"neutral\" && doc.subjectivity == \"subjective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            },
            "neuobj":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"neutral\" && doc.subjectivity == \"objective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            },
            "negsub":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"negative\" && doc.subjectivity == \"subjective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            },
            "negobj":{
                "map":"function(doc){ if (doc.created_at > "+ starttime +  " && doc.created_at <"+ endtime +" && doc.polarity == \"negative\" && doc.subjectivity == \"objective\") emit(doc.lga_code, 1);}",
                "reduce":"function (key, values) {  return sum(values); }"
            }
        }
        db['_design/example3'] = dict(language='javascript', views=viewData)

        possub_view = db.view('example3/possub',group = True)
        posobj_view = db.view('example3/posobj',group = True)
        neusub_view = db.view('example3/neusub',group = True)
        neuobj_view = db.view('example3/neuobj',group = True)
        negsub_view = db.view('example3/negsub',group = True)
        negobj_view = db.view('example3/negobj',group = True)

        new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
        new_lga_name = ['Banyule', 'Bayside','Boroondara','Brimbank','Cardinia','Casey','Darebin','Frankston','Glen Eira','Greater Dandenong','Hobsons Bay','Hume','Knox','Macedon Ranges','Manningham','Maribyrnong','Maroondah','Melbourne','Melton','Mitchell','Monash','Moonee Valley','Moorabool','Moreland','Mornington Peninsula','Murrindindi','Nillumbik','Port Phillip','Stonnington','Whitehorse','Whittlesea','Wyndham','Yarra','Yarra Ranges']
        lgaid_i_map = {"20660": 0, "20910": 1, "21110": 2, "21180": 3, "21450": 4, "21610": 5, "21890": 6, "22170": 7, "22310": 8, "22670": 9, "23110": 10, "23270": 11, "23670": 12, "24130": 13, "24210": 14, "24330": 15, "24410": 16, "24600": 17, "24650": 18, "24850": 19, "24970": 20, "25060": 21, "25150": 22, "25250": 23, "25340": 24, "25620": 25, "25710": 26, "25900": 27, "26350": 28, "26980": 29, "27070": 30, "27260": 31, "27350": 32, "27450": 33}

        possub_result = processview(possub_view)
        posobj_result = processview(posobj_view)
        neusub_result = processview(neusub_view)
        neuobj_result = processview(neuobj_view)
        negsub_result = processview(negsub_view)
        negobj_result = processview(negobj_view)

        anlgajson = {
            "name":"null",
            "value":0,
            "children":[
                {
                    "name":"positive",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                },
                {
                    "name":"neutral",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                },
                {
                    "name":"negative",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                }
            ]
        }

        api3 = {
            "data":[
                {
                    "name":"melb",
                    "children":[]
                }
            ]
        }
        
        # final
        final_result = helper.get_scores_from_cached_data(starttime, endtime)

        lga_value_list = []

        for lga in query_lga:
    
            index = lgaid_i_map[str(lga)]    
            newlgajson = copy.deepcopy(anlgajson)
    
            newlgajson["children"][0]["value"] = possub_result[index] + posobj_result[index] + final_result[str(lga)]['children']['children'][0]['value']
            newlgajson["children"][0]["children"][0]["value"] = possub_result[index] + final_result[str(lga)]['children']['children'][0]['children'][0]['value']
            newlgajson["children"][0]["children"][1]["value"] = posobj_result[index] + final_result[str(lga)]['children']['children'][0]['children'][1]['value']
            newlgajson["children"][1]["value"] = neusub_result[index] + neuobj_result[index] + final_result[str(lga)]['children']['children'][1]['value']
            newlgajson["children"][1]["children"][0]["value"] = neusub_result[index] + final_result[str(lga)]['children']['children'][1]['children'][0]['value']
            newlgajson["children"][1]["children"][1]["value"] = neuobj_result[index] + final_result[str(lga)]['children']['children'][1]['children'][1]['value']
            newlgajson["children"][2]["value"] = negsub_result[index] + negobj_result[index] + final_result[str(lga)]['children']['children'][2]['value']
            newlgajson["children"][2]["children"][0]["value"] = negsub_result[index] + final_result[str(lga)]['children']['children'][2]['children'][0]['value']
            newlgajson["children"][2]["children"][1]["value"] = negobj_result[index] + final_result[str(lga)]['children']['children'][2]['children'][1]['value']
            newlgajson["value"] = newlgajson["children"][0]["value"] + newlgajson["children"][1]["value"] + newlgajson["children"][2]["value"] 
            newlgajson["name"] = new_lga_name[index]
            data = copy.deepcopy(newlgajson)
            lga_value_list.append(data)
        api3["data"][0]["children"] = lga_value_list

        return json.dumps(api3, ensure_ascii=False)



def processview(view):
    new_lga_id = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
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




@server.errorhandler(400)
def bad_request(e):
    err = {}
    err["name"] = "400"
    err["message"] = "Unauthorized."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(403)
def forbidden(e):
    err = {}
    err["name"] = "403"
    err["message"] = "Forbidden."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(404)
def handle_404_error(e):
    err = {}
    err["name"] = "404 Not Found"
    err["message"] = "The requested URL was not found on the server."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(405)
def method_not_allowed(e):
    err = {}
    err["name"] = "405"
    err["message"] = "Illegalmethod."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(500)
def internal_server_error(e):
    err = {}
    err["name"] = "500"
    err["message"] = "An internal server error occurred."
    return json.dumps(err, ensure_ascii=False)
    

server.run(port = 6100,debug = True,host = '0.0.0.0',threaded = True)
